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
    
    def can_swap(self, candy_1_coords: tuple[int, int], candy_2_coords: tuple[int, int]) -> bool:
        horizontal_difference = abs(candy_1_coords[0] - candy_2_coords[0])
        vertical_difference = abs(candy_1_coords[1] - candy_2_coords[1])
        candies_are_bordering = (
            horizontal_difference + vertical_difference == 1
        )

        candy_1_value = self.grid[candy_1_coords[0]][candy_1_coords[1]]
        candy_2_value = self.grid[candy_2_coords[0]][candy_2_coords[1]]
        candies_share_color = candy_1_value == candy_2_value

        # TODO: check also that swapping triggers cascade ak
        # gives score and so not just swaps two candies.
        return candies_are_bordering and not candies_share_color

    def swap(self, candy_1_coords: tuple[int, int], candy_2_coords: tuple[int, int]):
        candy_1_value = self.grid[candy_1_coords[0]][candy_1_coords[1]]
        candy_2_value = self.grid[candy_2_coords[0]][candy_2_coords[1]]

        self.grid[candy_1_coords[0]][candy_1_coords[1]] = candy_2_value
        self.grid[candy_2_coords[0]][candy_2_coords[1]] = candy_1_value
    
    def cascade(self):
        raise NotImplementedError()

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
