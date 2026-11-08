#!/usr/bin/env python3
import abc
from .creature import Creature
from .monsters import FireBase, FireEvolved, MorphBase, MorphEvolved


class CreatureFactory(abc.ABC):
    @abc.abstractmethod
    def create_base(self) -> Creature:
        pass

    @abc.abstractmethod
    def create_evolved(self) -> Creature:
        pass


class FlameFactory(CreatureFactory):
    def create_base(self) -> FireBase:
        return FireBase()

    def create_evolved(self) -> FireEvolved:
        return FireEvolved()


class TransformCreatureFactory(CreatureFactory):
    def create_base(self) -> MorphBase:
        return MorphBase()

    def create_evolved(self) -> MorphEvolved:
        return MorphEvolved()
