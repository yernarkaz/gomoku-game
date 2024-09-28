# entry point to run the game

from classes.game import Game

print(__name__)
if __name__ == "__main__":
    game = Game()
    game.run()
