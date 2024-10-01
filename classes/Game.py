from .board import Board
from .player import Player
from .stone import Stone


class Game:
    def __init__(self, config: dict):
        self.game_mode = config["game_mode"]  # switch game modes
        self.board = Board(config["board_config"])

        if self.game_mode == "hvh":
            self.board.player_black = Player(
                config=config["player_config"], stone_color="B"
            )
            self.board.player_white = Player(
                config=config["player_config"], stone_color="W"
            )

            self.board.current_player = (
                self.board.player_black
            )  # Player with black starts the game
        else:
            pass

    def run(self) -> None:
        print("Game is started, enjoy!")
        print(f"Mode: {self.game_mode}")
        print("-----------------------")

        while True:
            player_input = input(
                f"Please enter x and y coordinates for player with {self.board.current_player.stone_color} color "
                "stones in the form of <x><space><y>:\n"
            )

            try:
                parsed_input = player_input.split(" ")
                x, y = int(parsed_input[0]), int(parsed_input[1])

                new_stone = Stone(
                    x,
                    y,
                    self.board.current_player.stone_color,
                    self.board.current_player,
                )
                self.board.add_stone(new_stone)

                board_state = self.board.check_win_condition()

                if board_state:
                    print(
                        f"Player with {self.board.winner.stone_color} stones won the game."
                    )
                    exit()

                print("-----------------------")
                print(self.board)
                print("-----------------------")
            except Exception as e:
                print(str(e))
                print("-----------------------")
