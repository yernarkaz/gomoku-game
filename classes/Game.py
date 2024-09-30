from .board import Board
from .player import Player


class Game:
    def __init__(self, config: dict):
        game_mode = config["game_mode"]  # switch game modes
        self.board = Board(config["board_config"])

        if game_mode == "hvh":
            self.player_black = Player()
            self.player_white = Player()

    def run(self) -> None:
        print("Game is started")

        print("Board status")
        print(self.board)
