from .stone import Stone


class Board:
    def __init__(self, config: dict):
        self.n = config["n_cells"]
        self.board = [
            [Stone(None, x=x, y=y) for x in range(self.n)] for y in range(self.n)
        ]

        self.player_black = None
        self.player_white = None
        self.current_player = None

        self.winner = None
        self.last_move = None

    def update_board(self, stone: Stone) -> None:
        if not 0 <= stone.x < self.n or not 0 <= stone.y < self.n:
            return False

        # set the stone to the board according to it's coordinate
        if self.board[stone.x][stone.y].player:
            return False

        self.board[stone.x][stone.y] = stone
        self.current_player = (
            self.player_white
            if self.current_player.stone_color == self.player_black.stone_color
            else self.player_black
        )

        return True

    def __str__(self) -> str:
        return "\n".join(
            [" ".join([str(stone) for stone in row]) for row in self.board]
        )
