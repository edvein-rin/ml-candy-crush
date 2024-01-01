from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Tuple


@dataclass
class Model(ABC):
    rows_number: int
    columns_number: int
    colors_number: int

    @abstractmethod
    def find_optimal_movement(
        self,
        game_field: List[List[int]],
        turns_left=1,
    ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        "Finds optimal movement on `game_field` and returns a tuple of two coordinates of candies to switch."
        pass
