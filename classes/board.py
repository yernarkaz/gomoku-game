from typing import List, Tuple

from .player import Player
from .stone import Stone


class Board:
    """
    Represents the game board for the Gomoku game.
    """

    def __init__(self, config: dict):
        self._n = config["n_cells"]
        self._n_win = config["n_win"]
        self._target_depth = config["heuristics_target_depth"]
        self._score_win = config["heuristics_score_win"]
        self._score_loose = config["heuristics_score_loose"]

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

    @property
    def size(self) -> int:
        """Returns the size of the board."""
        return self._n

    @property
    def nwin(self) -> int:
        """Returns the number of stones in a row needed to win."""
        return self._n_win

    @property
    def target_depth(self) -> int:
        """Returns the target depth for the AI."""
        return self._target_depth

    @property
    def score_win(self) -> int:
        """Returns the score for a win."""
        return self._score_win

    @property
    def score_loose(self) -> int:
        """Returns the score for a loss."""
        return self._score_loose

    @property
    def board(self) -> List[List[Stone]]:
        """Returns the current state of the board."""
        return self._board

    @board.setter
    def board(self, _board: List[List[Stone]]):
        """Sets the current state of the board."""
        self._board = _board

    def is_visited(self, x: int, y: int) -> bool:
        """
        Check if the cell at the given coordinates has been visited.

        Args:
            x (int): The x-coordinate of the cell.
            y (int): The y-coordinate of the cell.

        Returns:
            bool: True if the cell has been visited, False otherwise.
        """
        return self._board[x][y].visited

    def put_stone(self, x: int, y: int) -> bool:
        """
        Places a stone on the board at the specified coordinates.

        Args:
            x (int): The x-coordinate on the board.
            y (int): The y-coordinate on the board.

        Returns:
            bool: True if the stone was successfully placed, False if the position was already occupied.
        """
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
        """
        Retrieve a list of coordinates (x, y) for all unvisited stones on the board.

        Returns:
            List[Tuple[int]]: A list of tuples where each tuple contains the x and y
            coordinates of an unvisited stone.
        """
        return [
            (stone.x, stone.y)
            for row in self._board
            for stone in row
            if not stone.visited
        ]

    def get_left_stones(self) -> int:
        """
        Get the number of stones left on the board.

        Returns:
            int: The number of stones left.
        """
        return self._left_stones

    def toggle_player(self) -> None:
        """
        Switches the current player to the other player.

        This method toggles the current player between player_black and player_white
        based on the stone color of the current player.
        """
        toggle_flag = self.current_player.stone_color == self.player_black.stone_color
        self.current_player = self.player_white if toggle_flag else self.player_black

    def check_sliding_win_condition(self, w: List[Stone]) -> bool:
        """
        Check if there are `n_win` consecutive black or white stones in the given list.

        Args:
            w (List[Stone]): A list of Stone objects to check for a winning condition.

        Returns:
            bool: True if there are `n_win` consecutive stones of the same color, False otherwise.
        """

        all_black_stones = all(stone.color == "B" for stone in w)
        all_white_stones = all(stone.color == "W" for stone in w)

        if all_black_stones or all_white_stones:
            self.winner == self.current_player
            return True

    def check_rowwise_win_condition(self) -> Tuple[bool, Player]:
        """
        Checks for a winning condition in the board by examining each row.

        This method iterates through each row of the board and uses a sliding window
        approach to check for a sequence of stones that meet the winning condition.

        Returns:
            Tuple[bool, Player]: A tuple where the first element is a boolean indicating
            whether a winning condition was found, and the second element is the Player
            who won. If no winning condition is found, the second element is None.
        """
        # iterate each row.
        for i in range(self.size):
            # iterate via sliding window with the number of n_win stones.
            for j in range(self.size - self.nwin + 1):
                w = self._board[i][j : j + self.nwin]  # sliding window
                condition = self.check_sliding_win_condition(w)
                if condition:
                    return True, w[0].player

        return False, None

    def check_colwise_win_condition(self) -> bool:
        """
        Checks for a winning condition in the columns of the board.

        Iterates through each column and uses a sliding window approach to check
        for a sequence of stones that meet the winning condition.

        Returns:
            bool: True if a winning condition is found, False otherwise.
            player: The player who has won, or None if no winning condition is found.
        """
        # iterate each column.
        for j in range(self.size):
            # iterate via sliding window with the number of n_win stones.
            for i in range(self.size - self.nwin + 1):
                w = [self._board[i + k][j] for k in range(self.nwin)]
                condition = self.check_sliding_win_condition(w)
                if condition:
                    return True, w[0].player

        return False, None

    def check_diagwise_win_condition(self) -> bool:
        """
        Check for a win condition diagonally on the board.

        This method checks if there are `n_win` stones of the same color in a row
        diagonally in any direction on the board. It iterates through all possible
        diagonal lines on the board and checks for the win condition using the
        `check_sliding_win_condition` method.

        Returns:
            tuple: A tuple containing a boolean and a player object. The boolean
            indicates whether a win condition is met (True) or not (False). If a
            win condition is met, the player object represents the player who won.
            If no win condition is met, the player object is None.
        """
        # n_win is the number of stones of the same color in a row to win
        # check if there are n_win black or white stones in a row in any direction of any diagonals

        for j in range(self.size):
            # skip if there is less than n_win number of stones to check
            if self.size - j < self.nwin:
                continue

            for i in range(self.size - self.nwin + 1):
                if i + j + self.nwin > self.size:
                    continue

                w_diag_right = [self._board[k + i][k + i + j] for k in range(self.nwin)]
                w_diag_right_mirror = [
                    self._board[k + i + j][k + i] for k in range(self.nwin)
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
                    self._board[self.size - k - i - j - 1][k + i]
                    for k in range(self.nwin)
                ]
                w_diag_left_mirror = [
                    self._board[k + i][self.size - k - i - j - 1]
                    for k in range(self.nwin)
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
        Checks if there is a winning condition on the board.

        This method checks for a win condition by evaluating the board
        diagonally, row-wise, and column-wise. If a win condition is found
        in any of these directions, it sets the winner attribute to the
        corresponding player and returns True. If no win condition is found,
        it returns False.

        Returns:
            bool: True if a win condition is found, False otherwise.
        """

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
