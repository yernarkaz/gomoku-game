from .player import Player


class Board:
    def __init__(self, config: dict):
        n = config["n_cells"]
        self.board = [[" " for _ in range(n)] for _ in range(n)]

        self.current_player = None
        self.winner = None
        self.last_move = None

    def set_player_move(self, player: Player) -> None:
        self.current_player = player
        if self.current_player.stone_color == "black":
            pass
        else:
            pass

    def __str__(self) -> str:
        return "\n".join([" ".join(row) for row in self.board])
