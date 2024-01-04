import sys

sys.path.append("..")

from models.DQN.dqn_model import DQNModel
from models.greedy.greedy_model import GreedyModel
from models.q_learn.q_learn_model import QLearnModel
from game.game_field import GameField
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
def update_game_field(game_field: GameField, action):
    updated_game_field, broken_candies, combo = game_field.swap(
        action[0], action[1]
    ).cascade()
    reward = 10 * (broken_candies**2 - broken_candies) * combo

    return updated_game_field, reward


async def process_model(model, game_field: GameField, rounds_left, rewards):
    action = model.find_optimal_movement(game_field.grid, rounds_left)
    game_field, reward = update_game_field(game_field, action)
    rewards.append(reward)
    print(model.__class__.__name__, action, reward)


async def main():
    TOTAL_TURNS = 5

    models = {
        "DQN": DQNModel(ROWS_NUMBER, COLUMNS_NUMBER, COLORS_NUMBER),
        "QLearn": QLearnModel(ROWS_NUMBER, COLUMNS_NUMBER, COLORS_NUMBER),
        "Greedy": GreedyModel(ROWS_NUMBER, COLUMNS_NUMBER, COLORS_NUMBER),
    }

    initial_game_field = GameField(ROWS_NUMBER, COLUMNS_NUMBER, COLORS_NUMBER)
    initial_game_field, _, _ = initial_game_field.cascade()

    rewards = {model: [0] for model in models}  # To store rewards for each model
    game_fields = {
        model: initial_game_field for model in models
    }  # Separate game field for each model

    sorted_data = sorted(rewards.items(), key=lambda x: sum(x[1]), reverse=True)

    # Create a 2D array sorted by the sum of the lists
    array = [pair[1] for pair in sorted_data]

    rewards = {
        'DQN': array[0],
        'QLearn': array[1],
        'Greedy': array[2],
    }

    for turn in range(TOTAL_TURNS):
        turns_left = TOTAL_TURNS - turn
        print("------", "TURN", turn + 1, "------")
        await asyncio.gather(
            *(
                process_model(
                    models[model], game_fields[model], turns_left, rewards[model]
                )
                for model in models
            )
        )

    plot_cumulative_rewards(models, rewards)
    plot_total_rewards(models, rewards)


if __name__ == "__main__":
    asyncio.run(main())


