#!/usr/bin/env python3
import abc
import typing


class StrategyError(Exception):
    pass


class BattleStrategy(abc.ABC):
    @abc.abstractmethod
    def act(self, entity: typing.Any) -> list[str]:
        pass

    @abc.abstractmethod
    def is_valid(self, entity: typing.Any) -> bool:
        pass

    def check(self, entity: typing.Any) -> None:
        if not self.is_valid(entity):
            raise StrategyError(
                f"{self.__class__.__name__} is not valid for "
                f"{entity.__class__.__name__}")


class NormalStrategy(BattleStrategy):
    def is_valid(self, entity: typing.Any) -> bool:
        return (callable(getattr(entity, "attack", None)))

    def act(self, entity: typing.Any) -> list[str]:
        self.check(entity)
        return [entity.attack()]


class AggressiveStrategy(BattleStrategy):
    def is_valid(self, entity: typing.Any) -> bool:
        return (callable(getattr(entity, "transform", None))
                and callable(getattr(entity, "revert", None)))

    def act(self, entity: typing.Any) -> list[str]:
        self.check(entity)
        return [entity.transform(), entity.attack(), entity.revert()]
