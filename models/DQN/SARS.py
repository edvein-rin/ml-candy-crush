import models.DQN.utils as utils

import random
import numpy as np

NSARS = 25  # number of SARS' sequences to generate at each turn
DEPTH = 5  # max depth of SARS' sequence
DISCOUNT = 0.5

def get_sarsa_values(state, action, rows, cols, colors):
    return [generate_sarsa(state, action, rows, cols, colors) for _ in range(NSARS)]

def generate_sarsa(curr_state, action, rows, cols, colors):
    def make_switch(state, action):
        grid = np.array(state[0])
        coord1, coord2 = action
        grid[coord1], grid[coord2] = grid[coord2], grid[coord1]
        grid, turn_score = utils.cascade(grid, rows, cols, colors)
        return grid, turn_score

    prev_state = curr_state
    depth = DEPTH
    utility = 0
    depth = 0
    while (not utils.is_end_state(prev_state)) and depth < DEPTH:
        if depth != 0:
            action = random.choice(utils.actions(prev_state, rows, cols))
        grid, reward = make_switch(prev_state, action)
        new_state = (utils.arr_to_tuple(grid), prev_state[1] - 1)
        prev_state = new_state
        utility += reward * (DISCOUNT**depth)
        depth += 1
    return utility