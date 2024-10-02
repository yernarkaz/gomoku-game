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

            # Player with black stone starts the game
            self.board.current_player = self.board.player_black
        else:
            pass

    def run(self) -> None:
        print("Game is started, enjoy!")
        print(f"Mode: {self.game_mode}")
        print("-----------------------")

        while True:
            player_input = input(
                f"Please enter x and y coordinates for player with {self.board.current_player.get_color_desc()}"
                " stone in the form of <x><space><y>:\n"
            )

            try:
                if len(player_input.strip()) == 0:
                    raise ValueError("Empty input is invalid.")

                parsed_input = player_input.split(" ")
                if len(parsed_input) != 2:
                    raise ValueError(
                        f"The input should consist of x and y values between 0 and {self.board.n - 1}"
                    )

                try:
                    x, y = int(parsed_input[0]), int(parsed_input[1])
                except Exception:
                    raise ValueError(
                        f"The input should consist of x and y values between 0 and {self.board.n - 1}"
                    )

                new_stone = Stone(
                    x,
                    y,
                    self.board.current_player.stone_color,
                    self.board.current_player,
                )
                self.board.add_stone(new_stone)

                win_condition = self.board.check_win_condition()
                if win_condition:
                    print(
                        f"Player with {self.board.winner.get_color_desc()} stone color won the game."
                    )
                    exit()

                self.board.toggle_player()

                print("-----------------------")
                print(self.board)
                print("-----------------------")
            except Exception as e:
                print(str(e))
                print("-----------------------")
