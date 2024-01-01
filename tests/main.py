import sys

sys.path.append("..")

from models.DQN.dqn_model import DQNModel
from models.greedy.greedy_model import GreedyModel
from models.q_learn.q_learn_model import QLearnModel
from plots import plot_cumulative_rewards, plot_total_rewards

import random
import asyncio

ROWS_NUMBER = 9
COLUMNS_NUMBER = 9
COLORS_NUMBER = 5

# DUMMY FUNC, REPLACE
def init_game_field():
    return [
        [random.randint(1, COLORS_NUMBER) for _ in range(COLUMNS_NUMBER)]
        for _ in range(ROWS_NUMBER)
    ]

# DUMMY FUNC, REPLACE
def update_game_field(game_field, action):
    game_field = init_game_field()
    reward = 100*random.randint(1, 10)
    return game_field, reward


async def process_model(model, game_field, rounds_left, rewards):
    action = model.find_optimal_movement(game_field, rounds_left)
    game_field, reward = update_game_field(game_field, action)
    rewards.append(reward)
    print(model, action, reward)


async def main():
    TOTAL_ROUNDS = 2

    models = {
        "DQN": DQNModel(ROWS_NUMBER, COLUMNS_NUMBER, COLORS_NUMBER),
        "QLearn": QLearnModel(ROWS_NUMBER, COLUMNS_NUMBER, COLORS_NUMBER),
        "Greedy": GreedyModel(ROWS_NUMBER, COLUMNS_NUMBER, COLORS_NUMBER),
    }

    initial_game_field = init_game_field()

    rewards = {model: [0] for model in models}  # To store rewards for each model
    game_fields = {model: initial_game_field for model in models}  # Separate game field for each model


    for round in range(TOTAL_ROUNDS):
        rounds_left = TOTAL_ROUNDS - round
        print(round)
        await asyncio.gather(*(process_model(models[model], game_fields[model], rounds_left, rewards[model]) for model in models))

    
    plot_cumulative_rewards(models, rewards)
    plot_total_rewards(models, rewards)


if __name__ == "__main__":
    asyncio.run(main())
