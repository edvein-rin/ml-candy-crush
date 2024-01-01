import random
import numpy as np
import collections

from models.model import Model


class QLearn(Model):
    def __init__(self, n_features, n_sars, depth, num_samples, n_turns, n_rows, n_cols, n_colors, discount, step_size, epsilon, weights):
        self.NFEATURES = n_features
        self.NSARS = n_sars
        self.DEPTH = depth
        self.NUMSAMPLES = num_samples
        self.NTURNS = n_turns
        self.NROWS = n_rows
        self.NCOLS = n_cols
        self.NCOLORS = n_colors
        self.DISCOUNT = discount
        self.STEP_SIZE = step_size
        self.EPSILON = epsilon
        self.weights = weights

    def dot_product(self, a, b):
        return sum(a[i] * b[i] for i in range(len(a)))

    def arr_to_tuple(self, arr):
        tup_arr = [tuple(elem) for elem in arr]
        return tuple(tup_arr)

    def is_end_state(self, state):
        return state[1] == 0

    def actions(self, state):
        actions = []
        game_field = state[0]
        for i in range(self.NROWS):
            for j in range(self.NCOLS):
                if self.is_valid_move(game_field, (i, j), (i, j + 1)):
                    coord1 = (i, j)
                    coord2 = (i, j + 1)
                    actions.append((coord1, coord2))
                elif self.is_valid_move(game_field, (i, j), (i + 1, j)):
                    coord1 = (i, j)
                    coord2 = (i + 1, j)
                    actions.append((coord1, coord2))
        return actions

    def drop_cols(self, game_field, cols_to_rows_map):
        for col in cols_to_rows_map:
            curr_rows = cols_to_rows_map[col]
            min_row = curr_rows[0]
            max_row = curr_rows[1]
            diff = max_row - min_row + 1
            for i in range(min_row):
                game_field[min_row - 1 - i + diff,
                           col] = game_field[min_row - 1 - i, col]
            for i in range(diff):
                game_field[i, col] = random.randint(1, self.NCOLORS)

    def explore_coord(self, game_field, i, j):
        color = game_field[i, j]
        color_rows_set = set([(i, j)])
        color_cols_set = set([(i, j)])
        for row in range(i):
            if color != game_field[i - row - 1, j]:
                break
            color_rows_set.add((i - row - 1, j))
        for row in range(i + 1, self.NROWS):
            if color != game_field[row, j]:
                break
            color_rows_set.add((row, j))
        for col in range(j):
            if color != game_field[i, j - col - 1]:
                break
            color_cols_set.add((i, j - col - 1))
        for col in range(j + 1, self.NCOLS):
            if color != game_field[i, col]:
                break
            color_cols_set.add((i, col))
        return color_rows_set, color_cols_set

    def cascade_coords(self, game_field):
        coords = set()
        for i in range(self.NROWS):
            for j in range(self.NCOLS):
                color_rows_set, color_cols_set = self.explore_coord(
                    game_field, i, j)
                color_all_set = set()
                if len(color_rows_set) >= 3:
                    color_all_set = color_rows_set
                if len(color_cols_set) >= 3:
                    color_all_set = color_all_set.union(color_cols_set)
                if len(color_all_set) > len(coords):
                    coords = color_all_set
        return coords

    def cascade(self, game_field):
        turn_score = 0
        combo = 1
        while True:
            coords = self.cascade_coords(game_field)
            cascade_size = len(coords)
            if cascade_size < 3:
                break
            add_score = 10 * (cascade_size ** 2 - cascade_size) * combo
            turn_score += add_score
            cols_to_rows_map = {}
            for coord in coords:
                if coord[1] not in cols_to_rows_map:
                    cols_to_rows_map[coord[1]] = [coord[0], coord[0]]
                else:
                    curr_rows = cols_to_rows_map[coord[1]]
                    curr_row_min = curr_rows[0]
                    curr_row_max = curr_rows[1]
                    if coord[0] < curr_row_min:
                        curr_rows[0] = coord[0]
                    elif coord[0] > curr_row_max:
                        curr_rows[1] = coord[0]
            self.drop_cols(game_field, cols_to_rows_map)
        return game_field, turn_score

    def test_switch(self, state, action):
        game_field = np.array(state[0])
        coord1, coord2 = action
        game_field[coord1], game_field[coord2] = game_field[coord2], game_field[coord1]
        coords = self.cascade_coords(game_field)
        return len(coords)

    def max_count(self, state):
        game_field = np.array(state[0])
        row_count = collections.Counter()
        col_count = collections.Counter()
        max_row = []
        max_col = []
        for i in range(self.NROWS):
            for j in range(self.NCOLS):
                row_count[(i, game_field[i, j])] += 1
            max_row.append(max(row_count[(i, color)]
                           for color in range(1, self.NCOLORS)))
        for j in range(self.NCOLS):
            for i in range(self.NROWS):
                col_count[(j, game_field[i, j])] += 1
            max_col.append(max(col_count[(j, color)]
                           for color in range(1, self.NCOLORS)))
        return max_row + max_col

    def is_valid_coord(self, coord):
        if (coord[0] < 0 or coord[0] >= self.NROWS) or (coord[1] < 0 or coord[1] >= self.NCOLS):
            return False
        else:
            return True

    def is_valid_move(self, game_field, coord1, coord2):
        if coord1 == coord2:
            return False
        if self.is_valid_coord(coord1) and self.is_valid_coord(coord2):
            if (abs(coord1[0] - coord2[0]) == 1 and coord1[1] == coord2[1]) or (
                    abs(coord1[1] - coord2[1]) == 1 and coord1[0] == coord2[0]):
                game_field_copy = np.copy(game_field)
                game_field_copy[coord1], game_field_copy[coord2] = game_field_copy[coord2], game_field_copy[coord1]
                color_rows_set1, color_cols_set1 = self.explore_coord(
                    game_field_copy, coord1[0], coord1[1])
                if len(color_rows_set1) >= 3 or len(color_cols_set1) >= 3:
                    return True
                color_rows_set2, color_cols_set2 = self.explore_coord(
                    game_field_copy, coord2[0], coord2[1])
                if len(color_rows_set2) >= 3 or len(color_cols_set2) >= 3:
                    return True
        return False

    def num_valid_moves(self, game_field):
        count = 0
        for i in range(self.NROWS):
            for j in range(self.NCOLS):
                if self.is_valid_move(game_field, (i, j), (i, j + 1)) or self.is_valid_move(game_field, (i, j), (i + 1, j)):
                    count += 1
        return count

    def make_switch(self, state, action):
        game_field = np.array(state[0])
        coord1, coord2 = action
        game_field[coord1], game_field[coord2] = game_field[coord2], game_field[coord1]
        game_field, turn_score = self.cascade(game_field)
        return game_field, turn_score

    def generate_sarsa(self, curr_state, action):
        prev_state = curr_state
        depth = self.DEPTH
        utility = 0
        depth = 0
        while (not self.is_end_state(prev_state)) and depth < self.DEPTH:
            if depth != 0:
                action = random.choice(self.actions(prev_state))
            game_field, reward = self.make_switch(prev_state, action)
            new_state = (self.arr_to_tuple(game_field), prev_state[1] - 1)
            prev_state = new_state
            utility += reward * (self.DISCOUNT ** depth)
            depth += 1
        return utility

    def get_feature_vec(self, state, action):
        min_row = min(action[0][0], action[1][0])
        max_row = max(action[0][0], action[1][0])
        same_col = 1 if action[0][1] == action[1][1] else 0
        n_valid_moves = self.num_valid_moves(state[0])
        max_delete = self.test_switch(state, action)
        med_util = np.median([self.generate_sarsa(state, action)
                             for i in range(self.NSARS)])
        phi = [min_row, max_row, same_col, n_valid_moves, max_delete, med_util]
        phi += self.max_count(state)
        return np.array(phi)

    def get_q_opt(self, state, action):
        if self.is_end_state(state):
            return 0.
        return self.dot_product(self.get_feature_vec(state, action), self.weights)

    def find_optimal_movement(self, game_field, turn):
        action = None
        turns_left = self.NTURNS - turn
        curr_state = (self.arr_to_tuple(game_field), turns_left)
        if random.random() < self.EPSILON:
            action = random.choice(self.actions(curr_state))
        else:
            v_opt, pi_opt = max((self.get_q_opt(curr_state, action), action)
                                for action in self.actions(curr_state))
            action = pi_opt
        return action

# q_learning = QLearning(24, 25, 5, 10000, 50, 9, 9, 5, 0.5,
#                        0.00000000001, 0.5, np.zeros(24, dtype=float))

# game_field = [[2, 5, 5, 2, 4, 3, 5, 2, 4],
#         [3, 2, 2, 1, 5, 1, 5, 5, 1],
#         [2, 2, 4, 4, 1, 3, 1, 5, 2],
#         [5, 1, 5, 2, 5, 1, 4, 3, 4],
#         [1, 3, 4, 5, 1, 2, 3, 3, 5],
#         [1, 4, 1, 5, 3, 3, 4, 5, 4],
#         [3, 5, 2, 1, 1, 4, 3, 1, 4],
#         [2, 3, 4, 3, 1, 2, 5, 3, 5],
#         [4, 2, 4, 2, 5, 3, 2, 3, 4]]

# action = q_learning.find_optimal_movement(game_field, 1)
# print(action) 
