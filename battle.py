#!/usr/bin/env python3
from ex3 import CreatureFactory, FlameFactory, TransformCreatureFactory


def test_factory(factory: CreatureFactory) -> None:
    base = factory.create_base()
    print(base.describe())
    print(base.attack())
    evolved = factory.create_evolved()
    print(evolved.describe())
    print(evolved.attack())


def test_battle(factory1: CreatureFactory, factory2: CreatureFactory) -> None:
    fighter1 = factory1.create_base()
    fighter2 = factory2.create_base()
    print(f"{fighter1.name} vs {fighter2.name}")
    print(fighter1.attack())
    print(fighter2.attack())


if __name__ == "__main__":
    flame_factory = FlameFactory()
    transform_factory = TransformCreatureFactory()
    print("Testing factory")
    test_factory(flame_factory)
    print()
    test_factory(transform_factory)
    print()
    print("Testing battle")
    test_battle(flame_factory, transform_factory)
