from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Character:
    """
    Represents a character in the game world.
    """

    character_id: int
    name: str
    role: str

    ambition: float = 0.5
    loyalty: float = 0.5

    is_player: bool = False

    relationships: dict[int, float] = field(default_factory=dict)
    memories: list[dict[str, Any]] = field(default_factory=list)

    # --------------------------------------------------
    # Relationships
    # --------------------------------------------------

    def set_relationship(
        self,
        character_id: int,
        value: float,
    ) -> None:
        self.relationships[character_id] = max(-1.0, min(1.0, value))

    def get_relationship(self, character_id: int) -> float:
        return self.relationships.get(character_id, 0.0)

    def modify_relationship(
        self,
        character_id: int,
        amount: float,
    ) -> None:
        current = self.get_relationship(character_id)
        self.set_relationship(character_id, current + amount)

    # --------------------------------------------------
    # Memories
    # --------------------------------------------------

    def add_memory(self, memory: dict[str, Any]) -> None:
        self.memories.append(memory)

    def forget_memories(self, count: int = 1) -> None:
        if count < 0:
            raise ValueError("Count cannot be negative.")

        del self.memories[:count]

    # --------------------------------------------------
    # Character attributes
    # --------------------------------------------------

    def modify_ambition(self, amount: float) -> None:
        self.ambition = max(0.0, min(1.0, self.ambition + amount))

    def modify_loyalty(self, amount: float) -> None:
        self.loyalty = max(0.0, min(1.0, self.loyalty + amount))
