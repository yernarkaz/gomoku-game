# entry point to run the game

from classes.game import Game
import os
import yaml

GAME_CONFIG_PATH = "config/game.yml"

if __name__ == "__main__":
    with open(os.path.join(os.path.dirname(__file__), GAME_CONFIG_PATH), "r") as file:
        game_config = yaml.safe_load(file)

    for config_name, path in game_config["config_paths"].items():
        with open(path, "r") as file:
            game_config[config_name] = yaml.safe_load(file)

    game = Game(game_config)
    game.run()
