import os

import yaml
from classes.game import Game

GAME_CONFIG_PATH = "config/game.yml"


def load_config(file_path):
    """
    Loads a YAML configuration file.

    Args:
        file_path (str): The path to the YAML configuration file.

    Returns:
        dict: The contents of the YAML file as a dictionary.

    Raises:
        ValueError: If the file cannot be read or parsed.
    """
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise ValueError(f"Failed to load config file: {e}")


if __name__ == "__main__":
    try:
        game_config = load_config(
            os.path.join(os.path.dirname(__file__), GAME_CONFIG_PATH)
        )

        for config_name, path in game_config["config_paths"].items():
            game_config[config_name] = load_config(path)

        game = Game(game_config)
        game.run()
    except Exception as e:
        print(f"Failed to start the game: {e}")
