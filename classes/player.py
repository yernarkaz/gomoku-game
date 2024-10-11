import random
from copy import deepcopy
from typing import TYPE_CHECKING, List, Tuple

if TYPE_CHECKING:
    from .board import Board
    from .player import Player, SmartPlayer

# Constants
WHITE = "W"
BLACK = "B"
UNDEFINED = "undefined"


class Player:
    """
    Represents a player in the Gomoku game.

    Attributes:
        stone_color (str): The color of the player's stones.
    """

    def __init__(self, stone_color: str):
        if stone_color not in {WHITE, BLACK}:
            raise ValueError(f"Invalid stone color: {stone_color}")
        self.stone_color = stone_color

    def get_color_desc(self) -> str:
        """
        Returns a descriptive string for the player's stone color.

        Returns:
            str: "white" if the stone color is white, "black" if black, otherwise "undefined".
        """
        if self.stone_color == WHITE:
            return "white"
        elif self.stone_color == BLACK:
            return "black"
        return UNDEFINED


class DumbPlayer(Player):
    """
    Represents a dumb player who makes random moves.

    Inherits from Player.
    """

    def __init__(self, stone_color: str):
        super().__init__(stone_color)

    def get_input(self, unvisited_xy_pairs: List[Tuple[int, int]]) -> str:
        """
        Returns a random move from the list of unvisited coordinates.

        Args:
            unvisited_xy_pairs (List[Tuple[int, int]]): List of unvisited (x, y) coordinate pairs.

        Returns:
            str: A string representing the chosen move in the format "x y".
        """
        x, y = random.choice(unvisited_xy_pairs)
        return f"{x} {y}"


class SmartPlayer(Player):
    """
    Represents a smart player who makes strategic moves.

    Inherits from Player.
    """

    def __init__(self, stone_color: str, opponent: "Player"):
        super().__init__(stone_color)
        self.opponent = opponent

    def set_move(self, i: int, j: int, board: "Board", player: "Player") -> None:
        """
        Sets a move on the board for the given player.

        Args:
            i (int): The row index on the board.
            j (int): The column index on the board.
            board (Board): The game board where the move is to be set.
            player (Player): The player making the move.

        Returns:
            None
        """

        board.board[i][j].player = player
        board.board[i][j].color = player.stone_color
        board.board[i][j].visited = True

    def unset_move(
        self,
        i: int,
        j: int,
        board: "Board",
    ):
        """
        Unsets a move on the board at the specified coordinates.

        This method resets the cell at the given (i, j) coordinates on the board
        to its initial state, indicating that no player has made a move there.

        Args:
            i (int): The row index of the cell to unset.
            j (int): The column index of the cell to unset.
            board (Board): The game board object containing the cell to unset.

        Returns:
            None
        """

        board.board[i][j].player = None
        board.board[i][j].color = "_"
        board.board[i][j].visited = False

    def is_unvisited_left(self, board: "Board") -> bool:
        """
        Check if there are any unvisited cells left on the board.

        Args:
            board (Board): The game board to check.

        Returns:
            bool: True if there is at least one unvisited cell, False otherwise.
        """

        for i in range(board.size):
            for j in range(board.size):
                if not board.is_visited(i, j):
                    return True

        return False

    def evaluate(self, board: "Board", depth: int) -> int:
        """
        Evaluate the current state of the board and return a score based on the game outcome.

        Args:
            board (Board): The current game board.
            depth (int): The depth of the game tree at the current state.

        Returns:
            int: A score representing the evaluation of the board state.
             If the game is won by the SmartPlayer, returns a positive score adjusted by depth.
             If the game is lost, returns a negative score adjusted by depth.
             Returns 0 if the game is not yet won or lost.
        """

        if board.check_win_condition():
            if type(board.winner) is SmartPlayer:
                return board.score_win - depth
            else:
                return board.score_loose + depth

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
        """
        Perform the minimax algorithm with alpha-beta pruning to determine the best move.

        Args:
            board (Board): The current state of the game board.
            depth (int): The current depth in the game tree.
            target_depth (int): The maximum depth to search in the game tree.
            is_maximizing (bool): True if the current move is for the maximizing player, False otherwise.
            alpha (int, optional): The best value that the maximizer currently can guarantee. Defaults to -float("inf").
            beta (int, optional): The best value that the minimizer currently can guarantee. Defaults to float("inf").

        Returns:
            int: The evaluated score of the board for the current move.
        """

        score = self.evaluate(board, depth)

        if depth == target_depth or score != 0:
            return score

        if not self.is_unvisited_left(board):
            return 0

        if is_maximizing:
            # Smart computer maximizes the score
            best_score = -float("inf")

            for i in range(board.size):
                for j in range(board.size):
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

            for i in range(board.size):
                for j in range(board.size):
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
        """
        Determines the optimal move for the player on the given board using the minimax algorithm.

        Args:
            board (Board): The current state of the game board.

        Returns:
            Tuple[int, int]: The coordinates of the optimal move as a tuple (row, column).
        """

        best_score = -float("inf")

        for i in range(board.size):
            for j in range(board.size):
                if not board.is_visited(i, j):
                    self.set_move(i, j, board, self)
                    score = self.minimax(board, 0, board.target_depth, False)
                    self.unset_move(i, j, board)

                    if score > best_score:
                        best_move = (i, j)
                        best_score = score

        return best_move

    def get_input(self, board: "Board") -> str:
        """
        Determines the optimal move for the player based on the current state of the board.

        This method uses a deep copy of the board to simulate the game tree and find the optimal move.
        Currently, it supports the following approaches:
        - Heuristics with minimax function and backtracking (Game tree)
        - Monte Carlo Tree search (not implemented)
        - Reinforcement learning (not implemented)

        Args:
            board (Board): The current state of the game board.

        Returns:
            str: The coordinates of the optimal move in the format "x y".
        """

        # 3 approaches to find the optimal move
        # approach1: Heuristics with minimax function and backtracking (Game tree)
        # approach2: Monte Carlo Tree search (not implemented)
        # approach2: Reinforcement learning (not implemented)

        board_ai = deepcopy(board)
        # pass the copy of board to the function
        # to simulate the game tree and find the optimal move.
        x, y = self.find_optimal_input(board_ai)
        return f"{x} {y}"
