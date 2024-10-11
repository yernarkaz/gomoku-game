import time
from typing import Tuple

from .board import Board
from .player import DumbPlayer, Player, SmartPlayer


class Game:
    """
    Represents the Gomoku game.

    Attributes:
        game_modes (dict): Configuration for different game modes.
        board (Board): The game board.
    """

    def __init__(self, config: dict):
        """
        Initializes the Game instance with the given configuration.

        Args:
            config (dict): Configuration dictionary containing game modes and board configuration.
        """
        self.game_modes = config["game_modes"]  # switch game modes
        self.board = Board(config["board_config"])

    def setup(self, game_mode: str) -> None:
        """
        Sets up the game based on the selected game mode.

        Args:
            game_mode (str): The game mode to set up. Can be "hvh" (Human vs Human), "hvd" (Human vs Dumb AI), or "hvai" (Human vs Smart AI).
        """
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
        """
        Returns a descriptive string for the current game mode.

        Returns:
            str: A descriptive string for the current game mode.
        """
        if self.game_mode == "hvh":
            return "Human vs Human"
        elif self.game_mode == "hvd":
            return "Human vs Dumb"
        else:
            return "Human vs AI/Smart"

    def validate_input(self, input) -> Tuple[int, int]:
        """
        Validates the input string for coordinates in the Gomoku game.

        Args:
            input (str): The input string containing the x and y coordinates separated by a space.

        Returns:
            Tuple[int, int]: A tuple containing the validated x and y coordinates as integers.

        Raises:
            ValueError: If the input is empty.
            ValueError: If the input does not contain exactly two values.
            ValueError: If the input values are not numeric.
            ValueError: If the input values are out of the valid range.
        """

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
        if not 0 <= x < self.board.size or not 0 <= y < self.board.size:
            raise ValueError(
                f"The x, y values ranges between 0"
                f" and {self.board.get_size() - 1}\n"
                f"Received input is ({x},{y})"
            )

        return x, y

    def handle_turn(self, x: int, y: int) -> bool:
        """
        Handles a player's turn by placing a stone on the board and checking for a win condition.

        Args:
            x (int): The x-coordinate where the stone is to be placed.
            y (int): The y-coordinate where the stone is to be placed.

        Returns:
            bool: True if the move results in a win condition, False otherwise.

        Raises:
            ValueError: If the position (x, y) is already occupied on the board.
        """
        if not self.board.put_stone(x, y):
            raise ValueError(f"The ({x},{y}) exists in the board.")

        win_condition = self.board.check_win_condition()
        if win_condition:
            return True

        self.board.toggle_player()

        return False

    def handle_player_input(self):
        """
        Handles the input for the current player based on their type.

        For a DumbPlayer, it retrieves input from the player's get_input method
        using the unvisited coordinates on the board.

        For a Player, it prompts the user to enter x and y coordinates.

        For a SmartPlayer, it retrieves input from the player's get_input method
        using the current board state and measures the time taken to compute the input.

        Returns:
            str: The input line representing the coordinates.
        """
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
            line_input = self.board.current_player.get_input(self.board, "advanced")
            print(self.board.weighted_score)
            print(self.board.pattern_score)
            elapsed_time = time.time() - start_time
            print(
                f"Smart computer input: {line_input}, elapsed time: {round(elapsed_time,1)} seconds"
            )
            print("-----------------------")
        return line_input

    def main_game_loop(self):
        """
        Main game loop that continuously handles player input and game turns.

        This method runs an infinite loop that:
        - Prompts the player for input.
        - Checks if the input is "exit" to terminate the game.
        - Validates the player's input.
        - Processes the player's turn and checks for a win condition.
        - If a player wins, announces the winner and exits the loop.
        - Catches and handles invalid input exceptions.

        Raises:
            ValueError: If the player's input is invalid.
        """
        while True:
            line_input = self.handle_player_input()

            if line_input.lower() == "exit":
                print("Exiting the game.")
                break

            try:
                x, y = self.validate_input(line_input)
                win_condition = self.handle_turn(x, y)
                print(self.board)
                print("-----------------------")
                if win_condition:
                    print(
                        f"Player with {self.board.winner.get_color_desc()} stone color won the game."
                    )
                    print(self.board)
                    break
            except ValueError as e:
                print(f"Invalid input: {e}")

    def start(self) -> None:
        """
        Starts the game by printing the initial game messages and entering the main game loop.

        This method performs the following actions:
        1. Prints a message indicating that the game has started.
        2. Prints the game mode description.
        3. Prints a separator line.
        4. Calls the main game loop to begin the game.

        Returns:
            None
        """
        print("Game is started, enjoy!")
        print(f"Mode: {self.get_game_mode_desc()}")
        print("-----------------------")

        self.main_game_loop()

    def run(self) -> None:
        """
        Runs the main loop of the Gomoku game.

        This method prints a welcome message and prompts the user to select a game mode.
        It continues to prompt the user until a valid game mode is entered.
        Once a valid game mode is selected, it sets up and starts the game.

        Returns:
            None
        """
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
