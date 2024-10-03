from .stone import Stone
from typing import List


class Board:
    def __init__(self, config: dict):
        self.n = config["n_cells"]
        self.n_win = config["n_win"]
        self.left_stones = self.n

        self.board = [
            [Stone(x=x, y=y, color="_", player=None) for x in range(self.n)]
            for y in range(self.n)
        ]

        self.player_black = None
        self.player_white = None
        self.current_player = None

        self.winner = None
        self.last_move = None
        self.history = []

    def get_size(self):
        return self.n

    def get_board(self):
        return self.board

    def add_stone(self, stone: Stone):
        # put the stone to the board according to it's coordinate
        if self.board[stone.x][stone.y].player:
            raise ValueError(f"The ({stone.x},{stone.y}) exists in the board.")

        self.board[stone.x][stone.y] = stone
        self.last_move = stone
        self.history.append(stone)
        self.left_stones -= 1

    def toggle_player(self):
        toggle_flag = self.current_player.stone_color == self.player_black.stone_color
        self.current_player = self.player_white if toggle_flag else self.player_black

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
            for j in range(self.n - self.n_win + 1):
                w = self.board[i][j : j + self.n_win]  # sliding window
                condition = self.check_sliding_win_condition(w)
                if condition:
                    return True

        return False

    def check_colwise_win_condition(self) -> bool:
        # iterate each column.
        for j in range(self.n):
            # iterate via sliding window with the number of n_win stones.
            for i in range(self.n - self.n_win + 1):
                w = [self.board[i + k][j] for k in range(self.n_win)]
                condition = self.check_sliding_win_condition(w)
                if condition:
                    return True

        return False

    def check_diagwise_win_condition(self) -> bool:

        # n_win is the number of stones of the same color in a row to win
        # check if there are n_win black or white stones in a row in any direction of any diagonals

        for j in range(self.n):

            # skip if there is less than n_win number of stones to check
            if self.n - j < self.n_win:
                continue

            for i in range(self.n - self.n_win + 1):

                if i + j + self.n_win > self.n:
                    continue

                w_diag_right = [self.board[k + i][k + i + j] for k in range(self.n_win)]
                w_diag_right_mirror = [
                    self.board[k + i + j][k + i] for k in range(self.n_win)
                ]

                # print(" ".join(str(i.x) + str(i.y) for i in w_diag_right))
                # print(" ".join(str(i.x) + str(i.y) for i in w_diag_right_mirror))

                condition_diag_right = self.check_sliding_win_condition(w_diag_right)
                condition_diag_mirror_right = self.check_sliding_win_condition(
                    w_diag_right_mirror
                )

                if condition_diag_right or condition_diag_mirror_right:
                    return True

                w_diag_left = [
                    self.board[self.n - k - i - j - 1][k + i] for k in range(self.n_win)
                ]
                w_diag_left_mirror = [
                    self.board[k + i][self.n - k - i - j - 1] for k in range(self.n_win)
                ]

                # print(" ".join(i.color for i in w_diag_left))
                # print(" ".join(i.color for i in w_diag_left_mirror))

                condition_diag_left = self.check_sliding_win_condition(w_diag_left)
                condition_diag_mirror_left = self.check_sliding_win_condition(
                    w_diag_left_mirror
                )

                if condition_diag_left or condition_diag_mirror_left:
                    return True

        return False

    def check_win_condition(self) -> bool:
        """
        9x9
        o x o o o o o o w
        o o x o o b o o w
        o o o x b o o o w
        o o o b x o o o w
        o o b o o x o o w
        o b o o o o o o o
        o o o o o o o o o
        o o o o o o o o o
        o o o o o o o o o
        """

        diag_status = self.check_diagwise_win_condition()
        row_status = self.check_rowwise_win_condition()
        col_status = self.check_colwise_win_condition()

        win_condition = diag_status or row_status or col_status

        if win_condition:
            self.winner = self.current_player

        return win_condition

    def __str__(self) -> str:
        return "\n".join(
            [" ".join([str(stone) for stone in row]) for row in self.board]
        )
