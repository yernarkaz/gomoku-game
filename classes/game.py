from typing import Tuple

from .board import Board
from .player import DumbPlayer, Player, SmartPlayer

import time


class Game:
    def __init__(self, config: dict):
        self.game_modes = config["game_modes"]  # switch game modes
        self.board = Board(config["board_config"])

    def setup(self, game_mode) -> None:
        self.game_mode = game_mode
        self.board.player_black = Player(stone_color="B")

        if self.game_mode == "hvh":
            self.board.player_white = Player(stone_color="W")

        elif self.game_mode == "hvd":
            self.board.player_white = DumbPlayer(stone_color="W")

        elif self.game_mode == "hvai":
            self.board.player_white = SmartPlayer(
                stone_color="W", opponent=self.board.player_black
            )

        # Player with black stone starts the game
        self.board.current_player = self.board.player_black

    def get_game_mode_desc(self) -> str:
        if self.game_mode == "hvh":
            return "Human vs Human"
        elif self.game_mode == "hvd":
            return "Human vs Dumb"
        else:
            return "Human vs AI/Smart"

    def validate_input(self, input) -> Tuple[int, int]:
        if len(input.strip()) == 0:
            raise ValueError("Empty input is invalid.")

        parsed_input = input.split(" ")
        if len(parsed_input) != 2:
            raise ValueError(
                f"The input should consist of x and y values between 0"
                f" and {self.board.get_size() - 1}"
            )

        x, y = parsed_input[0], parsed_input[1]
        if not x.isnumeric() or not y.isnumeric():
            raise ValueError(
                f"The input should consist of x and y values between 0"
                f" and {self.board.get_size() - 1}"
            )

        x, y = int(x), int(y)
        if not 0 <= x < self.board.get_size() or not 0 <= y < self.board.get_size():
            raise ValueError(
                f"The x, y values ranges between 0"
                f" and {self.board.get_size() - 1}\n"
                f"Received input is ({x},{y})"
            )

        return x, y

    def handle_turn(self, x: int, y: int) -> bool:
        if not self.board.put_stone(x, y):
            raise ValueError(f"The ({x},{y}) exists in the board.")

        win_condition = self.board.check_win_condition()
        if win_condition:
            return True

        self.board.toggle_player()

        return False

    def start(self) -> None:
        print("Game is started, enjoy!")
        print(f"Mode: {self.get_game_mode_desc()}")
        print("-----------------------")

        while True:
            try:
                print(f"#{self.board.get_left_stones()} stones are left to put.")
                if self.board.get_left_stones() == 0:
                    print("Draw, game is over.")
                    print("See you next time!")
                    exit()

                if type(self.board.current_player) is DumbPlayer:
                    line_input = self.board.current_player.get_input(
                        self.board.get_unvisited_xy_pairs()
                    )
                    print(f"Dumb computer input: {line_input}")
                elif type(self.board.current_player) is Player:
                    line_input = input(
                        f"Please enter x and y coordinates for player with"
                        f" {self.board.current_player.get_color_desc()}"
                        " stone in the form of <x><space><y>:\n"
                    )
                elif type(self.board.current_player) is SmartPlayer:
                    print("Smart computer is thinking...")
                    start_time = time.time()
                    line_input = self.board.current_player.get_input(self.board)
                    elapsed_time = time.time() - start_time
                    print(
                        f"Smart computer input: {line_input}, elpased time: {elapsed_time} seconds"
                    )

                if line_input.lower() == "exit":
                    exit()

                x, y = self.validate_input(line_input)
                win_condition = self.handle_turn(x, y)
                if win_condition:
                    print(
                        f"Player with {self.board.winner.get_color_desc()}"
                        "stone color won the game."
                    )
                    print(self.board)
                    exit()

                print("-----------------------")
                print(self.board)
                print("-----------------------")
            except Exception as e:
                print(f"Exception occured: {e}")

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
