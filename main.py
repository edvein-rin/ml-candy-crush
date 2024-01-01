import random
import pprint

from models.greedy.greedy_model import GreedyModel
from models.q_learn.q_learn_model import QLearnModel
from models.DQN.dqn_model import DQNModel

printer = pprint.PrettyPrinter()

ROWS_NUMBER = 9
COLUMNS_NUMBER = 9
COLORS_NUMBER = 5


def main():
    game_field = [
        [random.randint(1, COLORS_NUMBER) for _ in range(COLUMNS_NUMBER)]
        for _ in range(ROWS_NUMBER)
    ]

    print("-" * 9, "Game field", "-" * 9)
    printer.pprint(game_field)

    greedy_model = GreedyModel(ROWS_NUMBER, COLUMNS_NUMBER, COLORS_NUMBER)
    q_learn_model = QLearnModel(ROWS_NUMBER, COLUMNS_NUMBER, COLORS_NUMBER)
    dqn_model = DQNModel(ROWS_NUMBER, COLUMNS_NUMBER, COLORS_NUMBER)
    print()
    print("GreedyModel best movement:", greedy_model.find_optimal_movement(game_field))
    print("QLearn best movement:", q_learn_model.find_optimal_movement(game_field))
    print("DQN best movement:", dqn_model.find_optimal_movement(game_field))


if __name__ == "__main__":
    main()
