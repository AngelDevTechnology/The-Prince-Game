from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum

from engine.models.character import Character


class Role(IntEnum):
    PEASANT = 1
    COURTIER = 2
    ADVISOR = 3
    KING = 4


@dataclass(slots=True)
class Complot:
    initiator: Character
    target: Character

    success: bool | None = None
    chance: float = 0.0

    def __post_init__(self) -> None:
        self.chance = self.success_chance()

    def success_chance(self) -> float:
        """
        Calculate the probability of a successful conspiracy.

        A higher-ranking target makes the conspiracy harder.
        """
        grade_initiator = Role[self.initiator.role.upper()].value
        grade_target = Role[self.target.role.upper()].value

        gap = grade_target - grade_initiator

        return max(0.0, min(100.0, 50.0 - 15.0 * gap))

    def __repr__(self) -> str:
        return (
            f"Complot("
            f"initiator={self.initiator.name!r}, "
            f"target={self.target.name!r}, "
            f"chance={self.chance:.1f}%, "
            f"success={self.success}"
            f")"
        )
