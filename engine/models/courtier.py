from dataclasses import dataclass

from engine.models.character import Character


@dataclass(slots=True)
class Courtier(Character):
    """
    Represents a courtier in the royal court.
    """

    influence: float = 0.0

    def __post_init__(self) -> None:
        if not 0.0 <= self.influence <= 100.0:
            raise ValueError("Influence must be between 0 and 100.")

    def modify_influence(self, amount: float) -> None:
        self.influence = max(
            0.0,
            min(100.0, self.influence + amount),
        )

    def __repr__(self) -> str:
        return (
            f"Courtier("
            f"id={self.character_id}, "
            f"name={self.name!r}, "
            f"role={self.role!r}, "
            f"ambition={self.ambition}, "
            f"loyalty={self.loyalty}, "
            f"influence={self.influence}"
            f")"
        )
