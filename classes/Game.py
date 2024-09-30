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
        print("Game is started")
        print(f"Mode: {self.game_mode}")

        while True:
            player_input = input(
                f"Player with {self.board.current_player.stone_color} color "
                "enter x and y coordinates as the form of <x>,<y>:"
            )

            try:
                parsed_input = player_input.split(",")
                x, y = int(parsed_input[0]), int(parsed_input[1])

                new_stone = Stone(self.board.current_player, x, y)
                success = self.board.update_board(new_stone)

                if not success:
                    raise ValueError(
                        f"The current stone at {x},{y} is already set in the board."
                    )
                else:
                    print()
                    print(self.board)
                    print()
            except Exception as e:
                print(f"The given input:{player_input} is wrong, try gain.")
                print(str(e))
