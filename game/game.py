import pygame
from typing import Union

from game.game_field import GameField
from game.assets import Assets, Asset

from game.constants import ROWS_NUMBER, COLUMNS_NUMBER, COLORS_NUMBER, CANDY_SIZE


class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("ML Candy Crush")

        self.__screen = pygame.display.set_mode(
            (ROWS_NUMBER * CANDY_SIZE, COLUMNS_NUMBER * CANDY_SIZE + 40)
        )
        self.__clock = pygame.time.Clock()
        self.__font = pygame.font.Font(pygame.font.get_default_font(), 28)

        self.__assets = Assets()

    def __select_candy(self, row: int, column: int):
        if self.__selected_candy:
            if self.__selected_candy[0] == row and self.__selected_candy[1] == column:
                self.__selected_candy = None
            else:
                horizontal_difference = abs(self.__selected_candy[0] - row)
                vertical_difference = abs(self.__selected_candy[1] - column)

                can_swap = horizontal_difference + vertical_difference == 1
                if can_swap:
                    self.__field.swap(self.__selected_candy, (row, column))
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
        pass

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

        # Score label
        self.__screen.blit(
            self.__font.render("Score: %s" % self.__score, True, (255, 255, 255)),
            (8, self.__screen.get_height() - 28 - 12 / 2),
        )

        pygame.display.flip()

    def __loop(self):
        self.__handle_input()
        self.__update()
        self.__render()

        self.__clock.tick(60)

    def start(self):
        self.__field = GameField(ROWS_NUMBER, COLUMNS_NUMBER, COLORS_NUMBER)
        self.__selected_candy: Union[tuple[int, int], None] = None
        self.__score = 0

        while True:
            self.__loop()

    def stop(self):
        pygame.quit()
        raise SystemExit
