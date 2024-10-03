import random
from typing import List


class Player:

    def __init__(self, stone_color: str):
        self.stone_color = stone_color

    def get_color_desc(self):
        if self.stone_color == "W":
            return "white"
        elif self.stone_color == "B":
            return "black"

        return "undefined"


class DumbPlayer(Player):

    def __init__(self, stone_color: str):
        super().__init__(stone_color)

    def get_input(self, board: List[List[int]]) -> str:
        xy_pairs = [
            (stone.x, stone.y) for row in board for stone in row if stone.color == "_"
        ]

        n = len(xy_pairs)
        x, y = xy_pairs[random.randint(0, n - 1)]
        return f"{x} {y}"
