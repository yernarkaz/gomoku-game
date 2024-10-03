from .player import Player


class Stone:

    def __init__(
        self,
        x: int,
        y: int,
        color: str,
        player: Player,
    ):
        self.x = x
        self.y = y
        self.color = color
        self.player = player

    def __str__(self) -> str:
        return f"{self.color}"
