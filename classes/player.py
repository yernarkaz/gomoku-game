import random
from typing import List, Tuple


class Player:

    def __init__(self, stone_color: str):
        self.stone_color = stone_color

    def get_color_desc(self) -> str:
        if self.stone_color == "W":
            return "white"
        elif self.stone_color == "B":
            return "black"

        return "undefined"


class DumbPlayer(Player):

    def __init__(self, stone_color: str):
        super().__init__(stone_color)

    def get_input(self, unvisited_xy_pairs: List[Tuple[int, int]]) -> str:
        x, y = unvisited_xy_pairs[random.randint(0, len(unvisited_xy_pairs) - 1)]
        return f"{x} {y}"


class SmartPlayer(Player):
    def __init__(self, stone_color: str):
        super().__init__(stone_color)

    def get_input(self, board) -> str:
        # xy_pairs = [
        #     (stone.x, stone.y)
        #     for row in board.get_board()
        #     for stone in row
        #     if not stone.visited
        # ]

        # n = len(xy_pairs)

        # TODO AI
        # approach1: heuristics - Easy lvl
        # approach2: classic ML - Medium lvl
        # approach3: Reinforcement learning - Hard lvl

        # return f"{x} {y}"
        return ""
