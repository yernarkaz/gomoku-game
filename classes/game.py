from .board import Board
from .player import Player, DumbPlayer
from .stone import Stone


class Game:
    def __init__(self, config: dict):
        self.game_modes = config["game_modes"]  # switch game modes
        self.board = Board(config["board_config"])

    def setup(self, game_mode):
        self.game_mode = game_mode
        self.board.player_black = Player(stone_color="B")

        if self.game_mode == "hvh":
            self.board.player_white = Player(stone_color="W")

        elif self.game_mode == "hvd":
            self.board.player_white = DumbPlayer(stone_color="W")

        elif self.game_mode == "hvai":
            self.board.player_white = None  # TODO AI/Smart player

        # Player with black stone starts the game
        self.board.current_player = self.board.player_black

    def start(self):
        print("Game is started, enjoy!")
        print(f"Mode: {self.game_mode}")
        print("-----------------------")

        while True:
            xy_input = input(
                f"Please enter x and y coordinates for player with {self.board.current_player.get_color_desc()}"
                " stone in the form of <x><space><y>:\n"
            )

            try:
                if len(xy_input.strip()) == 0:
                    raise ValueError("Empty input is invalid.")

                parsed_input = xy_input.split(" ")
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

    def run(self) -> None:
        print("Welcome to Gomoku game!")

        game_modes_str = ", ".join(self.game_modes)

        while True:
            game_mode = input(f"Please type one of the game modes: {game_modes_str}:\n")

            if game_mode not in self.game_modes:
                print(f"The game mode {game_mode} is invalid. Type appropriate one.")
            else:
                break

        self.setup(game_mode)
        self.start()
