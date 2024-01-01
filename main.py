import random
import pprint

from models.random.random_model import RandomModel

printer = pprint.PrettyPrinter()


def main():
    game_field = [[random.randint(1, 6) for _ in range(9)] for _ in range(9)]

    print("-" * 9, "Game field", "-" * 9)
    printer.pprint(game_field)

    random_model = RandomModel()
    print("\nRandom best movement:", random_model.find_optimal_movement(game_field))


if __name__ == "__main__":
    main()
