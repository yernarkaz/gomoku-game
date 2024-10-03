class Player:

    def __init__(self, stone_color: str):
        self.stone_color = stone_color

    def get_color_desc(self):
        if self.stone_color == "W":
            return "white"
        elif self.stone_color == "B":
            return "black"

        return "undefined"


class DumbPlayer(Player):

    def __init__(self):
        super(DumbPlayer, self)
