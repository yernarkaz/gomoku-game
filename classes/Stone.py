from .player import Player


class Stone:
    def __init__(self, player: Player, x: int, y: int):
        self.player = player
        self.x = x
        self.y = y

    def __str__(self) -> str:
        return (
            f"{(self.player.stone_color if self.player else ' ')}:({self.x},{self.y})"
        )
