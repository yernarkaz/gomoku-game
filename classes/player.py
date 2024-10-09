import math
import random
from copy import deepcopy
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from .board import Board
    from .player import Player, SmartPlayer


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
        x, y = random.choice(unvisited_xy_pairs)
        return f"{x} {y}"


class SmartPlayer(Player):
    def __init__(self, stone_color: str, opponent: "Player"):
        super().__init__(stone_color)
        self.opponent = opponent

    def set_move(self, i: int, j: int, board: "Board", player: "Player") -> None:
        board.get_board()[i][j].player = player
        board.get_board()[i][j].color = player.stone_color
        board.get_board()[i][j].visited = True

    def unset_move(
        self,
        i: int,
        j: int,
        board: "Board",
    ):
        board.get_board()[i][j].player = None
        board.get_board()[i][j].color = "_"
        board.get_board()[i][j].visited = False

    def is_unvisited_left(self, board: "Board") -> bool:
        n = board.get_size()
        for i in range(n):
            for j in range(n):
                if not board.is_visited(i, j):
                    return True

        return False

    def evaluate(self, board: "Board", depth: int) -> int:
        if board.check_win_condition():
            if type(board.winner) is SmartPlayer:
                return board.get_score_win() - depth
            else:
                return board.get_score_loose() + depth

        return 0

    def minimax(
        self,
        board: "Board",
        depth: int,
        target_depth: int,
        is_maximizing: bool,
        alpha: int = -float("inf"),
        beta: int = float("inf"),
    ) -> int:

        score = self.evaluate(board, depth)

        if depth == target_depth or score != 0:
            return score

        if not self.is_unvisited_left(board):
            return 0

        n = board.get_size()

        if is_maximizing:
            # Smart computer maximizes the score
            best_score = -float("inf")

            for i in range(n):
                for j in range(n):
                    if not board.is_visited(i, j):
                        self.set_move(i, j, board, self)
                        score = self.minimax(
                            board,
                            depth + 1,
                            target_depth,
                            not is_maximizing,
                            alpha,
                            beta,
                        )
                        best_score = max(best_score, score)
                        self.unset_move(i, j, board)

                        alpha = max(alpha, best_score)
                        if beta <= alpha:
                            break

            return best_score
        else:
            # Player for black minimizes the score
            best_score = float("inf")

            for i in range(n):
                for j in range(n):
                    if not board.is_visited(i, j):
                        self.set_move(i, j, board, self.opponent)
                        score = self.minimax(
                            board,
                            depth + 1,
                            target_depth,
                            not is_maximizing,
                            alpha,
                            beta,
                        )
                        best_score = min(best_score, score)
                        self.unset_move(i, j, board)

                        beta = min(beta, best_score)
                        if beta <= alpha:
                            break

            return best_score

    def find_optimal_input(self, board: "Board") -> Tuple[int, int]:
        best_score = -float("inf")
        n = board.get_size()
        target_depth = board.get_target_depth()

        for i in range(n):
            for j in range(n):
                if not board.is_visited(i, j):
                    self.set_move(i, j, board, self)
                    score = self.minimax(board, 0, target_depth, False)
                    self.unset_move(i, j, board)

                    if score > best_score:
                        best_move = (i, j)
                        best_score = score

        return best_move

    def get_input(self, board: "Board") -> str:
        # 3 approaches to find the optimal move
        # approach1: Heuristics with minimax function and backtracking (Game tree)
        # approach2: Monte Carlo Tree search (not implemented)
        # approach2: Reinforcement learning (not implemented)

        board_ai = deepcopy(board)
        # pass the copy of board to the function
        # to simulate the game tree and find the optimal move.
        x, y = self.find_optimal_input(board_ai)
        return f"{x} {y}"
