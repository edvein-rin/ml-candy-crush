from abc import ABC, abstractmethod
from typing import List, Tuple


class Model(ABC):
    @abstractmethod
    def find_optimal_movement(
        self,
        game_field: List[List[int]],
    ) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        "Finds optimal movement on `game_field` and returns a tuple of two coordinates of candies to switch."
        pass
