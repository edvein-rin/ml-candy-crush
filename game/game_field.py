import random
from copy import deepcopy
from typing import Self

import numpy as np


class GameField:
    rows_number: int
    columns_number: int
    colors_number: int
    grid: list[list[int]]

    def __init__(
        self,
        rows_number: int,
        columns_number: int,
        colors_number: int,
        grid: list[list[int]] = None,
    ):
        self.rows_number = rows_number
        self.columns_number = columns_number
        self.colors_number = colors_number
        self.grid = grid if grid else self.__generate_grid()

    def __generate_grid(self) -> list[list[int]]:
        return [self.__generate_row() for _ in range(self.rows_number)]

    def __generate_row(self) -> list[int]:
        return [
            random.randint(1, self.colors_number) for _ in range(self.columns_number)
        ]

    def can_swap(
        self, candy_1_coords: tuple[int, int], candy_2_coords: tuple[int, int]
    ) -> bool:
        "Checks whether two candies can be swapped."

        horizontal_difference = abs(candy_1_coords[0] - candy_2_coords[0])
        vertical_difference = abs(candy_1_coords[1] - candy_2_coords[1])
        candies_are_bordering = horizontal_difference + vertical_difference == 1

        candy_1_value = self.grid[candy_1_coords[0]][candy_1_coords[1]]
        candy_2_value = self.grid[candy_2_coords[0]][candy_2_coords[1]]
        candies_share_color = candy_1_value == candy_2_value

        will_have_a_match = self.swap(candy_1_coords, candy_2_coords).has_matches()

        return candies_are_bordering and not candies_share_color and will_have_a_match

    def swap(
        self, candy_1_coords: tuple[int, int], candy_2_coords: tuple[int, int]
    ) -> Self:
        "Swaps two candies on the game field. Doesn't mutate the game field."

        new_grid = deepcopy(self.grid)

        candy_1_value = new_grid[candy_1_coords[0]][candy_1_coords[1]]
        candy_2_value = new_grid[candy_2_coords[0]][candy_2_coords[1]]

        new_grid[candy_1_coords[0]][candy_1_coords[1]] = candy_2_value
        new_grid[candy_2_coords[0]][candy_2_coords[1]] = candy_1_value

        new_game_field = GameField(
            self.rows_number, self.columns_number, self.colors_number, new_grid
        )

        return new_game_field

    def find_matches(self):
        "Finds 3 in a row or 3 in a column candies of the same color."

        grid = self.grid

        matches: list[list[tuple[int, int]]] = []
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                is_three_in_a_row_matching_possible = j + 3 <= self.rows_number
                if is_three_in_a_row_matching_possible:
                    if grid[i][j] == grid[i][j + 1] == grid[i][j + 2]:
                        matches.append([(i, j), (i, j + 1), (i, j + 2)])

                is_three_in_a_column_matching_possible = i + 3 <= self.columns_number
                if is_three_in_a_column_matching_possible:
                    if grid[i][j] == grid[i + 1][j] == grid[i + 2][j]:
                        matches.append([(i, j), (i + 1, j), (i + 2, j)])

        return matches

    def has_matches(self):
        "Checks whether there are matches on the game field."

        return len(self.find_matches()) > 0

    def __waterfall_grid_nones(self, grid: list[list[int]]) -> list[list[int]]:
        new_grid = deepcopy(grid)

        for i, row in enumerate(new_grid):
            for j, value in enumerate(row):
                if value is None:
                    if i == 0:
                        new_grid[i][j] = random.randint(1, self.colors_number)
                    else:
                        new_grid[i][j] = new_grid[i - 1][j]
                        new_grid[i - 1][j] = None
                        return self.__waterfall_grid_nones(new_grid)

        return new_grid

    def cascade(self, broken_candies = 0, combo = 1):
        "Cascades game field. Doesn't mutate the game field."

        new_grid = deepcopy(self.grid)

        matches = self.find_matches()
        for match in matches:
            for candy_coords in match:
                broken_candies += 1
                new_grid[candy_coords[0]][candy_coords[1]] = None

        new_grid = self.__waterfall_grid_nones(new_grid)

        new_game_field = GameField(
            self.rows_number, self.columns_number, self.colors_number, new_grid
        )

        if new_game_field.has_matches():
            return new_game_field.cascade(broken_candies, combo + 1)

        return new_game_field, broken_candies, combo

    def __str__(self) -> str:
        return str(np.matrix(self.grid))

    def __repr__(self) -> str:
        return f"<GameField\n{np.matrix(self.grid)}>"


if __name__ == "__main__":
    game_field = GameField(4, 4, 5)

    print("Initial game field:")
    print(game_field)
    print()
    print("Matches:", game_field.find_matches())
    print()
    print("After cascade:")
    game_field_after_cascade = game_field.cascade()[0]
    print(game_field_after_cascade)
    print()
    print("Matches:", game_field_after_cascade.find_matches())
