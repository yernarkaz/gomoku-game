import random
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from .stone import Stone


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
        # x, y = unvisited_xy_pairs[random.randint(0, len(unvisited_xy_pairs) - 1)]
        x, y = random.choice(unvisited_xy_pairs)
        return f"{x} {y}"


class SmartPlayer(Player):
    def __init__(self, stone_color: str):
        super().__init__(stone_color)
        self.moves = []

    def get_optimal_move(
        self,
        smart_moves: List["Stone"],
        opponent_moves: List["Stone"],
        left_moves: List["Stone"],
        n: int,
        n_win: int,
    ) -> Tuple[int, int]:
        # Randomize the first move for the smart computer
        if len(opponent_moves) == 1:
            stone = random.choice(left_moves)
            return stone.x, stone.y

        for i in range(n):
            for j in range(n):
                pass
                # check if 2 stones in a row
                # check if 3 stones in a row
                # check if 4 stones in a row

        return 0, 0

    def get_input(
        self, _board: List[List["Stone"]], last_move: "Stone", n_win: int
    ) -> str:
        # TODO AI
        # approach1: heuristics - Basics with backtracking
        # approach2: Reinforcement learning

        """
        _ _ _ _ _
        _ _ _ _ _
        _ _ B _ _
        _ B _ W _
        _ _ _ _ _
        """
        opponent_moves = [
            stone for row in _board for stone in row if type(stone.player) is Player
        ]

        smart_moves = [
            stone
            for row in _board
            for stone in row
            if type(stone.player) is SmartPlayer
        ]

        left_moves = [stone for row in _board for stone in row if not stone.visited]

        x, y = self.get_optimal_move(
            smart_moves, opponent_moves, left_moves, len(_board[0]), n_win
        )

        return f"{x} {y}"
