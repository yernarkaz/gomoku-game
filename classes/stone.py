from typing import Optional

from classes.player import Player


class Stone:
    """
    Represents a stone in the Gomoku game.

    Attributes:
        x (int): The x-coordinate of the stone.
        y (int): The y-coordinate of the stone.
        color (str): The color of the stone, default is "_".
        player (Optional[Player]): The player who placed the stone, default is None.
        visited (bool): Flag to check if the stone has been visited, default is False.
    """

    def __init__(
        self,
        x: int,
        y: int,
        color: str = "_",
        player: Optional[Player] = None,
        visited: bool = False,
    ):
        self.x = x
        self.y = y
        self.color = color
        self.player = player
        self.visited = visited

    def __str__(self) -> str:
        return f"{self.color}"
