from models.model import Model
from models.DQN import utils, MLPRegressor, SARS

import numpy as np
import collections

net = MLPRegressor.net

class DQNModel(Model):
    def __suggest_optimal_move(self, grid, turns_left):
        current_state = (utils.arr_to_tuple(grid), turns_left)
        self.colors_number
        _, optimal_action = max(
            (self.__get_optimal_q_value(current_state, action), action) for action in utils.actions(current_state, self.rows_number, self.columns_number)
        )
        return optimal_action
    

    def __test_switch(self, state, action):
        grid = np.array(state[0])
        coord1, coord2 = action
        grid[coord1], grid[coord2] = grid[coord2], grid[coord1]
        coords = utils.cascade_coordinates(grid, self.rows_number, self.columns_number)
        return len(coords)


    def __max_count(self, state):
        grid = np.array(state[0])
        rowCount = collections.Counter()
        colCount = collections.Counter()
        max_row = []
        max_col = []
        for i in range(self.rows_number):
            for j in range(self.columns_number):
                rowCount[(i, grid[i, j])] += 1
            max_row.append(max(rowCount[(i, color)] for color in range(1, self.colors_number)))
        for j in range(self.columns_number):
            for i in range(self.rows_number):
                colCount[(j, grid[i, j])] += 1
            max_col.append(max(colCount[(j, color)] for color in range(1, self.colors_number)))
        return max_row + max_col


    def __num_valid_moves(self, grid):
        count = 0
        for i in range(self.rows_number):
            for j in range(self.columns_number):
                if utils.is_valid_move(grid, self.rows_number, self.columns_number, (i, j), (i, j + 1)) or utils.is_valid_move(
                    grid, self.rows_number, self.columns_number, (i, j), (i + 1, j)
                ):
                    count += 1
        return count


    def __get_optimal_q_value(self, state, action):
        def get_feature_vector(state, action):
            action1, action2 = action
            min_row = min(action1[0], action2[0])
            max_row = max(action1[0], action2[0])
            same_col = int(action1[1] == action2[1])
            n_valid_moves = self.__num_valid_moves(state[0])
            max_delete = self.__test_switch(state, action)

            sarsa_values = SARS.get_sarsa_values(state, action, self.rows_number, self.columns_number, self.colors_number) 
            med_util = np.median(sarsa_values)
            phi = [min_row, max_row, same_col, n_valid_moves, max_delete, med_util, *self.__max_count(state)]
            return np.array(phi)

        if utils.is_end_state(state):
            return 0.0
        return net.predict([get_feature_vector(state, action)])[0]
    
    
    def find_optimal_movement(self, game_field, turns_left=1):
        return self.__suggest_optimal_move(game_field, turns_left)