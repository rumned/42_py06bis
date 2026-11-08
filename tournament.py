#!/usr/bin/env python3
from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory
from ex4.strategy import (BattleStrategy, NormalStrategy,
                          AggressiveStrategy, StrategyError)


def battle(opponents: list[tuple[CreatureFactory, BattleStrategy]],
           evo: bool = False) -> None:
    fighters = []
    for factory, strategy in opponents:
        if evo is True:
            entity = factory.create_evolved()
        else:
            entity = factory.create_base()
        strategy.check(entity)
        fighters.append((entity, strategy))
    for i in range(len(fighters)):
        for j in range(i + 1, len(fighters)):
            entity_a, strategy_a = fighters[i]
            entity_b, strategy_b = fighters[j]
            print(f" Round {i}-{j}")
            print(f"{entity_a.describe()} vs {entity_b.describe()}")
            for line in strategy_a.act(entity_a) + strategy_b.act(entity_b):
                print(line)


if __name__ == "__main__":
    flame = FlameFactory()
    transform = TransformCreatureFactory()
    tournaments = [
        ("Tournament 1 (valid strat)",
         [(flame, NormalStrategy()),
          (transform, NormalStrategy()),
          (transform, AggressiveStrategy())],
         False),
        ("\nTournament 2 (invalid)",
         [(flame, AggressiveStrategy()),
          (transform, NormalStrategy())],
         False),
        ("\nTournament 3 (evolved)",
         [(flame, NormalStrategy()),
          (transform, NormalStrategy()),
          (transform, AggressiveStrategy())],
         True),
    ]
    for _ in range(3):
        for title, fighters, evolved in tournaments:
            try:
                print(title)
                battle(fighters, evolved)
            except StrategyError as e:
                print(f"Battle aborted: {e}")
