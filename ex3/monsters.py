#!/usr/bin/env python3
from .creature import Creature
from .transform import TransformCapability


class FireBase(Creature):
    def __init__(self, name: str = "Flameling") -> None:
        super().__init__(name, "Fire")

    def attack(self) -> str:
        return f"{self.name} uses Ember!"


class FireEvolved(Creature):
    def __init__(self, name: str = "Pyrodon") -> None:
        super().__init__(name, "Fire/Fighting")

    def attack(self) -> str:
        return f"{self.name} uses Fire Punch!"


class MorphBase(Creature, TransformCapability):
    def __init__(self, name: str = "Shiftling") -> None:
        super().__init__(name, "Normal")
        self.transformed = False

    def attack(self) -> str:
        if self.transformed:
            return f"{self.name} uses Morph Strike!"
        return f"{self.name} uses Tackle!"

    def transform(self) -> str:
        self.transformed = True
        return f"{self.name} shifts into a sharper form!"

    def revert(self) -> str:
        self.transformed = False
        return f"{self.name} returns to normal."


class MorphEvolved(Creature, TransformCapability):
    def __init__(self, name: str = "Morphagon") -> None:
        super().__init__(name, "Normal/Soul Reaper")
        self.transformed = False

    def attack(self) -> str:
        if self.transformed:
            return f"{self.name} uses ~卍解: Senbonzakura Kageyoshi~"
        return f"{self.name} uses front slash!"

    def transform(self) -> str:
        self.transformed = True
        return f"{self.name} morphs into a Shinigami!"

    def revert(self) -> str:
        self.transformed = False
        return f"{self.name} returns to normal."
