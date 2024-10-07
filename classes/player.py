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
        # x, y = unvisited_xy_pairs[random.randint(0, len(unvisited_xy_pairs) - 1)]
        x, y = random.choice(unvisited_xy_pairs)
        return f"{x} {y}"


class SmartPlayer(Player):
    def __init__(self, stone_color: str, opponent: "Player"):
        super().__init__(stone_color)
        self.opponent = opponent

    def set_move(self, i: int, j: int, board: "Board", player: "Player") -> None:
        board.get_board()[i][j].player = player
        board.get_board()[i][j].color = self.stone_color
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

    def evaluate(self, board: "Board") -> int:
        if board.check_rowwise_win_condition():
            if type(board.current_player) is Player:
                return 10
            else:
                return -10

        if board.check_colwise_win_condition():
            if type(board.current_player) is Player:
                return 10
            else:
                return -10

        if board.check_diagwise_win_condition():
            if type(board.current_player) is Player:
                return 10
            else:
                return -10

        return 0

    def minimax(self, board: "Board", depth: int, current_player: "Player") -> int:
        score = self.evaluate(board)

        if score != 0:
            return score

        if not self.is_unvisited_left(board):
            return 0

        n = board.get_size()

        if type(current_player) in [Player, DumbPlayer]:
            best_score = -1000

            for i in range(n):
                for j in range(n):
                    if not board.is_visited(i, j):
                        # set the move
                        self.set_move(i, j, board, current_player)
                        # recursively call the minimax function
                        # to find the best move.
                        best_score = max(
                            best_score, self.minimax(board, depth + 1, self)
                        )
                        # backtrack/undo the move
                        self.unset_move(i, j, board)

            return best_score
        elif type(current_player) is SmartPlayer:
            best_score = 1000

            for i in range(n):
                for j in range(n):
                    if not board.is_visited(i, j):
                        self.set_move(i, j, board, current_player)
                        best_score = min(
                            best_score, self.minimax(board, depth + 1, self.opponent)
                        )
                        self.unset_move(i, j, board)

            return best_score

    def find_optimal_input(self, board: "Board") -> Tuple[int, int]:
        best_score = -10
        n = board.get_size()

        for i in range(n):
            for j in range(n):
                if not board.is_visited(i, j):
                    # set the player move
                    self.set_move(i, j, board, self)

                    # evaluate the minimax function for the current move
                    score = self.minimax(board, 0, self)

                    # backtrack/undo the player move
                    self.unset_move(i, j, board)

                    if score > best_score:
                        best_score = score
                        optimal_move = (i, j)

        return optimal_move

    def get_input(self, board: "Board") -> str:
        # TODO AI
        # approach1: Heuristics with minimax function and backtracking (Game tree)
        # approach2: Reinforcement learning (not implemented)

        board_ai = deepcopy(board)
        # pass the copy of board to the function
        # to simulate the game tree and find the optimal move.
        x, y = self.find_optimal_input(board_ai)
        return f"{x} {y}"
