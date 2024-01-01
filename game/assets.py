from enum import StrEnum

import pygame


class Asset(StrEnum):
    CANDY_1 = "assets/images/candies/1.png"
    CANDY_2 = "assets/images/candies/2.png"
    CANDY_3 = "assets/images/candies/3.png"
    CANDY_4 = "assets/images/candies/4.png"
    CANDY_5 = "assets/images/candies/5.png"
    CANDY_6 = "assets/images/candies/6.png"
    CANDY_7 = "assets/images/candies/7.png"
    CANDY_8 = "assets/images/candies/8.png"
    SELECTED_CANDY = "assets/images/selected-candy.png"


class Assets:
    def __init__(self) -> None:
        self.__assets = {
            asset_path: pygame.image.load(asset_path) for asset_path in Asset
        }

    def get(self, key: str):
        return self.__assets[key]
