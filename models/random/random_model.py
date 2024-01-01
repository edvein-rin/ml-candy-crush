import random

from models.model import Model


class RandomModel(Model):
    def find_optimal_movement(self, game_field, turns_left=1):
        cell_row = random.randint(0, self.rows_number)
        cell_column = random.randint(0, self.columns_number)

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
