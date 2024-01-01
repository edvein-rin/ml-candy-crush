import random
import numpy as np

from models.model import Model


class GreedyModel(Model):
    def drop_columns(self, game_field, colsToRowsMap):
        for col in colsToRowsMap:
            currRows = colsToRowsMap[col]
            minRow = currRows[0]
            maxRow = currRows[1]
            diff = maxRow - minRow + 1
            for i in range(minRow):
                game_field[minRow - 1 - i + diff, col] = game_field[minRow - 1 - i, col]
            for i in range(diff):
                game_field[i, col] = random.randint(1, self.colors_number)

    def explore_coord(self, game_field, i, j):
        color = game_field[i, j]
        colorRowsSet = set([(i, j)])
        colorColsSet = set([(i, j)])
        for row in range(i):
            if color != game_field[i - row - 1, j]:
                break
            colorRowsSet.add((i - row - 1, j))
        for row in range(i + 1, self.rows_number):
            if color != game_field[row, j]:
                break
            colorRowsSet.add((row, j))
        for col in range(j):
            if color != game_field[i, j - col - 1]:
                break
            colorColsSet.add((i, j - col - 1))
        for col in range(j + 1, self.columns_number):
            if color != game_field[i, col]:
                break
            colorColsSet.add((i, col))
        return colorRowsSet, colorColsSet

    def cascade_coords(self, game_field):
        coords = set()
        for i in range(self.rows_number):
            for j in range(self.columns_number):
                colorRowsSet, colorColsSet = self.explore_coord(game_field, i, j)
                colorAllSet = set()
                if len(colorRowsSet) >= 3:
                    colorAllSet = colorRowsSet
                if len(colorColsSet) >= 3:
                    colorAllSet = colorAllSet.union(colorColsSet)
                if len(colorAllSet) > len(coords):
                    coords = colorAllSet
        return coords

    def cascade(self, game_field):
        score = 0
        combo = 1
        while True:
            coords = self.cascade_coords(game_field)
            cascadeSize = len(coords)
            if cascadeSize < 3:
                break
            add_score = 10 * (cascadeSize**2 - cascadeSize) * combo
            score += add_score
            combo += 1
            colsToRowsMap = {}
            for coord in coords:
                if coord[1] not in colsToRowsMap:
                    colsToRowsMap[coord[1]] = [coord[0], coord[0]]
                else:
                    currRows = colsToRowsMap[coord[1]]
                    currRowMin = currRows[0]
                    currRowMax = currRows[1]
                    if coord[0] < currRowMin:
                        currRows[0] = coord[0]
                    elif coord[0] > currRowMax:
                        currRows[1] = coord[0]
            self.drop_columns(game_field, colsToRowsMap)

        return score, combo

    def check_coord_validity(self, coord):
        if (coord[0] < 0 or coord[0] >= self.rows_number) or (
            coord[1] < 0 or coord[1] >= self.columns_number
        ):
            return False
        else:
            return True

    def check_move_validity(self, game_field, coord1, coord2):
        if self.check_coord_validity(coord1) and self.check_coord_validity(coord2):
            if (abs(coord1[0] - coord2[0]) == 1 and coord1[1] == coord2[1]) or (
                abs(coord1[1] - coord2[1]) == 1 and coord1[0] == coord2[0]
            ):
                game_field_copy = np.copy(game_field)
                game_field_copy[coord1], game_field_copy[coord2] = (
                    game_field_copy[coord2],
                    game_field_copy[coord1],
                )
                colorRowsSet1, colorColsSet1 = self.explore_coord(
                    game_field_copy, coord1[0], coord1[1]
                )
                if len(colorRowsSet1) >= 3 or len(colorColsSet1) >= 3:
                    return True
                colorRowsSet2, colorColsSet2 = self.explore_coord(
                    game_field_copy, coord2[0], coord2[1]
                )
                if len(colorRowsSet2) >= 3 or len(colorColsSet2) >= 3:
                    return True
        return False

    def find_optimal_movement(self, game_field, steps_left=1):
        coord1 = ()
        coord2 = ()
        max_score = 0
        for i in range(self.rows_number):
            for j in range(self.columns_number):
                temp_game_field = np.array(game_field)
                if self.check_move_validity(game_field, (i, j), (i, j + 1)):
                    candidate_coord1 = (i, j)
                    candidate_coord2 = (i, j + 1)
                    (
                        temp_game_field[candidate_coord1],
                        temp_game_field[candidate_coord2],
                    ) = (
                        temp_game_field[candidate_coord2],
                        temp_game_field[candidate_coord1],
                    )
                    turn_score, combo = self.cascade(temp_game_field)
                    if turn_score > max_score:
                        max_score = turn_score
                        coord1 = candidate_coord1
                        coord2 = candidate_coord2
                elif self.check_move_validity(game_field, (i, j), (i + 1, j)):
                    candidate_coord1 = (i, j)
                    candidate_coord2 = (i + 1, j)
                    (
                        temp_game_field[candidate_coord1],
                        temp_game_field[candidate_coord2],
                    ) = (
                        temp_game_field[candidate_coord2],
                        temp_game_field[candidate_coord1],
                    )
                    turn_score, combo = self.cascade(temp_game_field)
                    if turn_score > max_score:
                        max_score = turn_score
                        coord1 = candidate_coord1
                        coord2 = candidate_coord2
        return (coord1, coord2)


if __name__ == "__main__":
    greedy = GreedyModel(9, 9, 5)

    game_field = [
        [2, 5, 5, 2, 4, 3, 5, 2, 4],
        [3, 2, 2, 1, 5, 1, 5, 5, 1],
        [2, 2, 4, 4, 1, 3, 1, 5, 2],
        [5, 1, 5, 2, 5, 1, 4, 3, 4],
        [1, 3, 4, 5, 1, 2, 3, 3, 5],
        [1, 4, 1, 5, 3, 3, 4, 5, 4],
        [3, 5, 2, 1, 1, 4, 3, 1, 4],
        [2, 3, 4, 3, 1, 2, 5, 3, 5],
        [4, 2, 4, 2, 5, 3, 2, 3, 4],
    ]

    game_field = np.array(game_field)

    optimal_movement = greedy.find_optimal_movement(game_field)
    print(optimal_movement)
