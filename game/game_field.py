import random
from copy import deepcopy
from typing import List, Self

import numpy as np


class GameField:
    rows_number: int
    columns_number: int
    colors_number: int
    grid: List[List[int]]

    def __init__(
        self,
        rows_number: int,
        columns_number: int,
        colors_number: int,
        grid: List[List[int]] = None,
    ):
        self.rows_number = rows_number
        self.columns_number = columns_number
        self.colors_number = colors_number
        self.grid = grid if grid else self.__generate_grid()

    def __generate_grid(self) -> List[int]:
        # TODO: make it generate such a grid so it has no 3 in a row or in a column.
        return [self.__generate_row() for _ in range(self.rows_number)]

    def __generate_row(self) -> List[int]:
        return [
            random.randint(1, self.colors_number) for _ in range(self.columns_number)
        ]

    def swap(self, candy_1_coords: tuple[int, int], candy_2_coords: tuple[int, int]):
        candy_1_value = self.grid[candy_1_coords[0]][candy_1_coords[1]]
        candy_2_value = self.grid[candy_2_coords[0]][candy_2_coords[1]]

        self.grid[candy_1_coords[0]][candy_1_coords[1]] = candy_2_value
        self.grid[candy_2_coords[0]][candy_2_coords[1]] = candy_1_value
    
    def cascade(self):
        raise NotImplementedError()

    # def generate_next_row(self) -> Self:
    #     new_grid = deepcopy(self.grid[:-1])
    #     new_grid.insert(0, self.__generate_row())

    #     return GameField(
    #         self.rows_number, self.columns_number, self.colors_number, new_grid
    #     )

    def __str__(self) -> str:
        return str(np.matrix(self.grid))

    def __repr__(self) -> str:
        return f"<GameField\n{np.matrix(self.grid)}>"


if __name__ == "__main__":
    game_field = GameField(3, 3, 5)

    print("Initial game field:")
    print(game_field)

    # print("Next row:")
    # print(game_field.generate_next_row())
