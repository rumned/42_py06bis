#!/usr/bin/env python3
from ex3 import TransformCreatureFactory


if __name__ == "__main__":
    factory = TransformCreatureFactory()
    for creature in (factory.create_base(), factory.create_evolved()):
        print(creature.describe())
        print(creature.attack())
        print(creature.transform())
        print(creature.attack())
        print(creature.revert())
        print()
