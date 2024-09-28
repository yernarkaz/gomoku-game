class Board:
    def __init__(self):
        self.board = [[" " for _ in range(15)] for _ in range(15)]
        self.winner = None
        self.last_move = None

    def __str__(self):
        return "\n".join([" ".join(row) for row in self.board])
