import random

from models.model import Model


class RandomModel(Model):
    def find_optimal_movement(self, game_field):
        rows_number = len(game_field)
        columns_number = len(game_field[0])

        cell_row = random.randint(0, rows_number)
        cell_column = random.randint(0, columns_number)

        if random.random() >= 0.5:
            return (
                (cell_row, cell_column),
                (cell_row - 1, cell_row),
            )
        else:
            return (
                (cell_row, cell_column),
                (cell_row, cell_row - 1),
            )
