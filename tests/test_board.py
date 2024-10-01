from classes.board import Board
from classes.board import Stone

import pytest
import random
import os
import yaml

GAME_CONFIG_PATH = "../config/game.yml"

with open(os.path.join(os.path.dirname(__file__), GAME_CONFIG_PATH), "r") as file:
    game_config = yaml.safe_load(file)

for config_name, path in game_config["config_paths"].items():
    with open(path, "r") as file:
        game_config[config_name] = yaml.safe_load(file)
        board_config = game_config["board_config"]

random.seed(42)


@pytest.fixture
def random_scenario_board():
    n = board_config["n_cells"]

    colors = ["B", "W", "_"]
    board = [
        [
            Stone(x=x, y=y, color=colors[random.randint(0, 2)], player=None)
            for x in range(n)
        ]
        for y in range(n)
    ]

    return board


def test_check_rowwise_win_condition(random_scenario_board):
    board = Board(game_config["board_config"])
    board.board = random_scenario_board
    print("-----------------------")
    print(board)
    print("-----------------------")

    assert board.check_rowwise_win_condition()


def test_check_colwise_win_condition(random_scenario_board):
    board = Board(game_config["board_config"])
    board.board = random_scenario_board

    print("-----------------------")
    print(board)
    print("-----------------------")

    assert board.check_colwise_win_condition()
