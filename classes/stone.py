from .player import Player


class Stone:

    def __init__(
        self,
        x: int,
        y: int,
        color: str = "_",
        player: Player = None,
        visited: bool = False,
    ):
        self.x = x
        self.y = y
        self.color = color
        self.player = player
        self.visited = visited

    def __str__(self) -> str:
        return f"{self.color}"
