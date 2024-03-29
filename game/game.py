import pygame
import random
from typing import Union

from game.game_field import GameField
from game.assets import Assets, Asset
from game.constants import ROWS_NUMBER, COLUMNS_NUMBER, COLORS_NUMBER, CANDY_SIZE
from models.model import Model
from models.greedy.greedy_model import GreedyModel
from models.DQN.dqn_model import DQNModel
from models.q_learn.q_learn_model import QLearnModel

MODEL_NAME_TO_COLOR = {
    "GreedyModel": (255, 0, 0),
    "QLearnModel": (0, 255, 0),
    "DQNModel": (0, 0, 255),
}


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("ML Candy Crush")

        self.__screen = pygame.display.set_mode(
            (ROWS_NUMBER * CANDY_SIZE, COLUMNS_NUMBER * CANDY_SIZE + 80)
        )
        self.__clock = pygame.time.Clock()
        self.__font = pygame.font.Font(pygame.font.get_default_font(), 28)

        self.__assets = Assets()

        self.__field = GameField(ROWS_NUMBER, COLUMNS_NUMBER, COLORS_NUMBER)
        if self.__field.has_matches():
            self.__field = self.__field.cascade()[0]

        self.__selected_candy: Union[tuple[int, int], None] = None
        self.__score = 0
        self.__turns_left = 10
        self.__turn = 1
        self.__models = [
            GreedyModel(ROWS_NUMBER, COLUMNS_NUMBER, COLORS_NUMBER),
            QLearnModel(ROWS_NUMBER, COLUMNS_NUMBER, COLORS_NUMBER),
            DQNModel(ROWS_NUMBER, COLUMNS_NUMBER, COLORS_NUMBER),
        ]
        self.__model_values = {}

    def __select_candy(self, row: int, column: int):
        if self.__selected_candy:
            if self.__selected_candy[0] == row and self.__selected_candy[1] == column:
                self.__selected_candy = None
            else:
                can_swap = self.__field.can_swap(self.__selected_candy, (row, column))
                if can_swap:
                    self.__turns_left -= 1
                    self.__turn += 1
                    self.__model_values = {}

                    self.__field = self.__field.swap(
                        self.__selected_candy, (row, column)
                    )
                    new_game_field, broken_candies, combo = self.__field.cascade()
                    self.__field = new_game_field
                    self.__score += 10 * (broken_candies**2 - broken_candies) * combo
                    self.__selected_candy = None
                else:
                    self.__selected_candy = (row, column)
        else:
            self.__selected_candy = (row, column)

    def __handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stop()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.stop()
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    candy_row = event.pos[1] // CANDY_SIZE
                    candy_column = event.pos[0] // CANDY_SIZE

                    if (
                        candy_row >= 0
                        and candy_row <= ROWS_NUMBER
                        and candy_column >= 0
                        and candy_column <= COLUMNS_NUMBER
                    ):
                        self.__select_candy(candy_row, candy_column)
                    else:
                        self.__selected_candy = None

    def __update(self):
        if self.__turns_left <= 0:
            # TODO: results screen.
            print(f"\nSCORE = {self.__score}")
            self.stop()

    def __render(self):
        self.__screen.fill("black")

        # Candies
        for i, row in enumerate(self.__field.grid):
            for j, candy in enumerate(row):
                candy_image = self.__assets.get(Asset[f"CANDY_{candy}"])

                self.__screen.blit(candy_image, (CANDY_SIZE * j, CANDY_SIZE * i))

        # Selected candy
        if self.__selected_candy:
            selected_candy_image = self.__assets.get(Asset.SELECTED_CANDY)
            self.__screen.blit(
                selected_candy_image,
                (
                    self.__selected_candy[1] * CANDY_SIZE,
                    self.__selected_candy[0] * CANDY_SIZE,
                ),
            )

        # Turns left
        self.__screen.blit(
            self.__font.render(
                f"Turns left: {self.__turns_left}", True, (255, 255, 255)
            ),
            (8, self.__screen.get_height() - (28 + 7) * 2),
        )

        # Score label
        self.__screen.blit(
            self.__font.render(f"Score: {self.__score}", True, (255, 255, 255)),
            (8, self.__screen.get_height() - (28 + 6)),
        )

        # Model hints
        for i, model in enumerate(self.__models):
            model_name = model.__class__.__name__
            color = MODEL_NAME_TO_COLOR[model_name]
            value = (
                self.__model_values[model_name]
                if model_name in self.__model_values
                else None
            )

            if value:
                for candy_coordinates in value:
                    size_coefficient = {0: 1, 1: 0.9, 2: 0.8}[i]
                    pygame.draw.rect(
                        self.__screen,
                        color,
                        pygame.Rect(
                            candy_coordinates[1] * CANDY_SIZE
                            + CANDY_SIZE / 2
                            - CANDY_SIZE * 0.5 / 2,
                            candy_coordinates[0] * CANDY_SIZE
                            + CANDY_SIZE / 2
                            - CANDY_SIZE * 0.5 / 2,
                            CANDY_SIZE * 0.5 * size_coefficient,
                            CANDY_SIZE * 0.5 * size_coefficient,
                        ),
                    )

            self.__screen.blit(
                self.__font.render(model_name[0], True, color),
                (
                    self.__screen.get_width() - 40 - i * 40,
                    self.__screen.get_height() - (28 + 6),
                ),
            )

        pygame.display.flip()

    def __post_render_update(self):
        to_print = False
        for model in self.__models:
            model_name = model.__class__.__name__
            if model_name not in self.__model_values:
                to_print = True
                self.__model_values[model_name] = model.find_optimal_movement(
                    self.__field.grid, self.__turns_left
                )
        if to_print:
            print(f"TURN {self.__turn} :", self.__model_values)

    def __loop(self):
        self.__handle_input()
        self.__update()
        self.__render()
        self.__post_render_update()

        self.__clock.tick(60)

    def start(self):
        while True:
            self.__loop()

    def stop(self):
        pygame.quit()
        raise SystemExit
