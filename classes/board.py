from typing import List, Tuple

from .player import Player
from .stone import Stone


class Board:
    def __init__(self, config: dict):
        self._n = config["n_cells"]
        self._n_win = config["n_win"]
        self._left_stones = self._n * self._n

        self._board = [
            [Stone(x=x, y=y, color="_", player=None) for y in range(self._n)]
            for x in range(self._n)
        ]

        self.player_black = None
        self.player_white = None
        self.current_player = None

        self.winner = None
        self.last_move = None
        self.history = []

    def get_size(self):
        return self._n

    def get_nwin(self):
        return self._n_win

    def get_board(self):
        return self._board

    def set_board(self, _board: List[List[Stone]]):
        self._board = _board

    def is_visited(self, x: int, y: int) -> bool:
        return self._board[x][y].visited

    def put_stone(self, x: int, y: int) -> bool:
        # put the stone to the board according to it's coordinate
        print(x, y, self._board[x][y])
        if self._board[x][y].visited:
            return False

        stone = self._board[x][y]
        stone.color = self.current_player.stone_color
        stone.player = self.current_player
        stone.visited = True

        self.last_move = stone
        self.history.append(stone)
        self._left_stones -= 1

        return True

    def get_unvisited_xy_pairs(self) -> List[Tuple[int]]:
        return [
            (stone.x, stone.y)
            for row in self._board
            for stone in row
            if not stone.visited
        ]

    def get_left_stones(self) -> int:
        return self._left_stones

    def toggle_player(self) -> None:
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

    def check_rowwise_win_condition(self) -> Tuple[bool, Player]:
        # iterate each row.
        for i in range(self.get_size()):
            # iterate via sliding window with the number of n_win stones.
            for j in range(self.get_size() - self.get_nwin() + 1):
                w = self._board[i][j : j + self.get_nwin()]  # sliding window
                condition = self.check_sliding_win_condition(w)
                if condition:
                    return True, w[0].player

        return False, None

    def check_colwise_win_condition(self) -> bool:
        # iterate each column.
        for j in range(self.get_size()):
            # iterate via sliding window with the number of n_win stones.
            for i in range(self.get_size() - self.get_nwin() + 1):
                w = [self._board[i + k][j] for k in range(self.get_nwin())]
                condition = self.check_sliding_win_condition(w)
                if condition:
                    return True, w[0].player

        return False, None

    def check_diagwise_win_condition(self) -> bool:
        # n_win is the number of stones of the same color in a row to win
        # check if there are n_win black or white stones in a row in any direction of any diagonals

        for j in range(self.get_size()):
            # skip if there is less than n_win number of stones to check
            if self.get_size() - j < self.get_nwin():
                continue

            for i in range(self.get_size() - self.get_nwin() + 1):
                if i + j + self.get_nwin() > self.get_size():
                    continue

                w_diag_right = [
                    self._board[k + i][k + i + j] for k in range(self.get_nwin())
                ]
                w_diag_right_mirror = [
                    self._board[k + i + j][k + i] for k in range(self.get_nwin())
                ]

                condition_diag_right = self.check_sliding_win_condition(w_diag_right)
                condition_diag_mirror_right = self.check_sliding_win_condition(
                    w_diag_right_mirror
                )

                if condition_diag_right:
                    return True, w_diag_right[0].player

                if condition_diag_mirror_right:
                    return True, w_diag_right_mirror[0].player

                w_diag_left = [
                    self._board[self.get_size() - k - i - j - 1][k + i]
                    for k in range(self.get_nwin())
                ]
                w_diag_left_mirror = [
                    self._board[k + i][self.get_size() - k - i - j - 1]
                    for k in range(self.get_nwin())
                ]

                condition_diag_left = self.check_sliding_win_condition(w_diag_left)
                condition_diag_mirror_left = self.check_sliding_win_condition(
                    w_diag_left_mirror
                )

                if condition_diag_left:
                    return True, w_diag_left[0].player

                if condition_diag_mirror_left:
                    return True, w_diag_left_mirror[0].player

        return False, None

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

        diag_status, diag_winner = self.check_diagwise_win_condition()
        row_status, row_winner = self.check_rowwise_win_condition()
        col_status, col_winner = self.check_colwise_win_condition()

        if diag_status:
            self.winner = diag_winner
        elif row_status:
            self.winner = row_winner
        elif col_status:
            self.winner = col_winner

        return diag_status or row_status or col_status

    def __str__(self) -> str:
        return "\n".join(
            ["  ".join([str(stone) for stone in row]) for row in self._board]
        )
