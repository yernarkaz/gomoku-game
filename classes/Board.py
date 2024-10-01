from .stone import Stone
from typing import List


class Board:
    def __init__(self, config: dict):
        self.n = config["n_cells"]
        self.n_win = config["n_win"]
        self.board = [
            [Stone(x=x, y=y, color="_", player=None) for x in range(self.n)]
            for y in range(self.n)
        ]

        self.player_black = None
        self.player_white = None
        self.current_player = None

        self.winner = None
        self.last_move = None

    def add_stone(self, stone: Stone):
        if not 0 <= stone.x < self.n or not 0 <= stone.y < self.n:
            raise ValueError(
                f"The following {stone.x},{stone.y} coordinates are invalid."
            )

        # put the stone to the board according to it's coordinate
        if self.board[stone.x][stone.y].player:
            raise ValueError(
                f"The following {stone.x},{stone.y} coordinates are in the board."
            )

        self.board[stone.x][stone.y] = stone
        self.current_player = (
            self.player_white
            if self.current_player.stone_color == self.player_black.stone_color
            else self.player_black
        )

    def check_sliding_win_condition(self, w: List[Stone]) -> bool:
        # check if there are n_win black or white stones in a row.

        all_black_stones = all(stone.color == "B" for stone in w)
        all_white_stones = all(stone.color == "W" for stone in w)

        # end the game if any of the conditions above satisfies the winner condition.
        if all_black_stones or all_white_stones:
            self.winner == self.current_player
            return True

    def check_rowwise_win_condition(self) -> bool:
        # iterate each row.
        for i in range(self.n):
            # iterate via sliding window with the number of n_win stones.
            for j in range(self.n - self.n_win):
                w = self.board[i][j : self.n_win]  # sliding window
                condition = self.check_sliding_win_condition(w)
                if condition:
                    return True

        return False

    def check_colwise_win_condition(self) -> bool:
        # iterate each column.
        for j in range(self.n):
            # iterate via sliding window with the number of n_win stones.
            for i in range(self.n - self.n_win):
                w = self.board[i : self.n_win][j]
                condition = self.check_sliding_win_condition(w)
                if condition:
                    return True

        return False

    def check_diagonalwise_win_condition(self) -> bool:

        # number of black or white stones on a diagonal
        n_black_stones = 0
        n_white_stones = 0

        # n_win is the number of stones of the same color to win
        # check if there are {n_win} black or white stones in any direction of diagonals
        for j in range(self.n):
            # keep track of the previous stone's color
            prev_stone_color = None

            # skip if there is less than n_win number of cells to check
            if self.n - j < self.n_win:
                continue

            for i in range(self.n - j):
                stone_color = self.board[i][j].player.stone_color
                if prev_stone_color and prev_stone_color == stone_color:
                    if prev_stone_color == "B":
                        n_black_stones += 1
                    else:
                        n_white_stones += 1

                    if n_black_stones == self.n_win or n_white_stones == self.n_win:
                        self.winner = self.current_player
                        return True
                else:
                    n_black_stones = 0
                    n_white_stones = 0

                prev_stone_color = stone_color
        return False

    def check_win_condition(self) -> bool:
        # check any win condition for diagonals

        """
        o x o o o o o o o
        o o x o o b o o o
        o o o x b o o o o
        o o o b x o o o o
        o o b o o x o o o
        o b o o o o o o o
        o o o o o o o o o
        o o o o o o o o o
        o o o o o o o o o

        [(0,1),(1,2), (2,3), (3,4), (4,5)]
        """

        # diag_status = self.check_diagonalwise_win_condition()
        row_status = self.check_rowwise_win_condition()
        # col_status = self.check_colwise_win_condition()

        # return diag_status and row_status and col_status
        return row_status

    def __str__(self) -> str:
        return "\n".join(
            [" ".join([str(stone) for stone in row]) for row in self.board]
        )
