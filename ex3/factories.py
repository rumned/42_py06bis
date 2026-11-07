#!/usr/bin/env python3
import abc
from .creature import Creature
from .monsters import Flameling, Pyrodon, Shiftling, Morphagon


class CreatureFactory(abc.ABC):
	@abc.abstractmethod
	def create_base(self) -> Creature:
		pass

	@abc.abstractmethod
	def create_evolved(self) -> Creature:
		pass


class FlameFactory(CreatureFactory):
	def create_base(self) -> Creature:
		return Flameling()

	def create_evolved(self) -> Creature:
		return Pyrodon()


class TransformCreatureFactory(CreatureFactory):
	def create_base(self) -> Creature:
		return Shiftling()

	def create_evolved(self) -> Creature:
		return Morphagon()