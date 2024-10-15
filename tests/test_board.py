import os
import random

import pytest
import yaml
from classes.board import Board, Stone

GAME_CONFIG_PATH = "../config/game.yml"

with open(os.path.join(os.path.dirname(__file__), GAME_CONFIG_PATH), "r") as file:
    game_config = yaml.safe_load(file)

for config_name, path in game_config["config_paths"].items():
    with open(path, "r") as file:
        game_config[config_name] = yaml.safe_load(file)
        board_config = game_config["board_config"]

# random.seed(42)


@pytest.fixture
def random_scenario_board():
    n = board_config["n_cells"]

    colors = ["B", "W", "_"]
    _board = [
        [
            Stone(x=x, y=y, color=colors[random.randint(0, 2)], player=None)
            for x in range(n)
        ]
        for y in range(n)
    ]

    return _board


def test_rowwise_win_condition1(random_scenario_board):
    board = Board(game_config["board_config"])

    for j in range(board.nwin):
        random_scenario_board[0][j].color = "B"

    board.board = random_scenario_board
    print("-----------------------")
    print(board)
    print("-----------------------")

    assert board.check_rowwise_win_condition()


def test_rowwise_win_condition2(random_scenario_board):
    board = Board(game_config["board_config"])

    for j in range(board.nwin):
        random_scenario_board[board.size - 1][board.size - j - 1].color = "B"

    board.board = random_scenario_board
    print("-----------------------")
    print(board)
    print("-----------------------")

    assert board.check_rowwise_win_condition()


def test_rowwise_win_condition3(random_scenario_board):
    board = Board(game_config["board_config"])

    i = random.randint(0, board.size - 1)
    k = random.randint(0, board.size - board.nwin)
    colors = ["B", "W"]
    c = colors[random.randint(0, 1)]

    for j in range(k, k + board.nwin):
        random_scenario_board[i][j].color = c

    board.board = random_scenario_board
    print("-----------------------")
    print(board)
    print("-----------------------")

    assert board.check_rowwise_win_condition()


def test_colwise_win_condition1(random_scenario_board):
    board = Board(game_config["board_config"])

    for i in range(board.nwin):
        random_scenario_board[i][0].color = "W"

    board.board = random_scenario_board

    print("-----------------------")
    print(board)
    print("-----------------------")

    assert board.check_colwise_win_condition()


def test_colwise_win_condition2(random_scenario_board):
    board = Board(game_config["board_config"])

    for i in range(board.nwin):
        random_scenario_board[board.size - i - 1][board.size - 1].color = "W"

    board.board = random_scenario_board

    print("-----------------------")
    print(board)
    print("-----------------------")

    assert board.check_colwise_win_condition()


def test_colwise_win_condition3(random_scenario_board):
    board = Board(game_config["board_config"])

    j = random.randint(0, board.size - 1)
    k = random.randint(0, board.size - board.nwin)
    colors = ["B", "W"]
    c = colors[random.randint(0, 1)]

    for i in range(k, k + board.nwin):
        random_scenario_board[i][j].color = c

    board.board = random_scenario_board

    print("-----------------------")
    print(board)
    print("-----------------------")

    assert board.check_colwise_win_condition()


def test_diagwise_win_condition1(random_scenario_board):
    board = Board(game_config["board_config"])

    for i in range(board.nwin):
        random_scenario_board[i][i].color = "B"

    board.board = random_scenario_board

    print("-----------------------")
    print(board)
    print("-----------------------")

    assert board.check_diagwise_win_condition()


def test_diagwise_win_condition2(random_scenario_board):
    board = Board(game_config["board_config"])

    for i in range(board.nwin):
        random_scenario_board[i][board.size - i - 1].color = "W"

    board.board = random_scenario_board

    print("-----------------------")
    print(board)
    print("-----------------------")

    assert board.check_diagwise_win_condition()


def test_diagwise_win_condition3(random_scenario_board):
    board = Board(game_config["board_config"])

    for i in range(board.nwin):
        random_scenario_board[board.size - i - 1][board.size - i - 1].color = "W"

    board.board = random_scenario_board

    print("-----------------------")
    print(board)
    print("-----------------------")

    assert board.check_diagwise_win_condition()


def test_diagwise_win_condition4(random_scenario_board):
    board = Board(game_config["board_config"])

    for i in range(board.nwin):
        random_scenario_board[board.size - i - 1][i].color = "W"

    board.board = random_scenario_board

    print("-----------------------")
    print(board)
    print("-----------------------")

    assert board.check_diagwise_win_condition()


def test_diagwise_win_condition5(random_scenario_board):
    board = Board(game_config["board_config"])

    direction = random.randint(0, 3)
    k = random.randint(0, board.size - board.nwin)
    colors = ["B", "W"]
    c = colors[random.randint(0, 1)]

    for i in range(k, k + board.nwin):
        if direction == 0:
            random_scenario_board[i][i].color = c
        elif direction == 1:
            random_scenario_board[i][board.size - i - 1].color = c
        elif direction == 2:
            random_scenario_board[board.size - i - 1][i].color = "W"
        else:
            random_scenario_board[board.size - i - 1][board.size - i - 1].color = "W"

    board.board = random_scenario_board

    print("-----------------------")
    print(f"color: {c}, k: {k}, direction: {direction}")
    print(board)
    print("-----------------------")

    assert board.check_diagwise_win_condition()


def test_board_weights():
    board = Board(game_config["board_config"])
    weights = [
        [1, 2, 3, 4, 4, 4, 3, 2, 1],
        [2, 3, 4, 5, 5, 5, 4, 3, 2],
        [3, 4, 5, 6, 6, 6, 5, 4, 3],
        [4, 5, 6, 7, 7, 7, 6, 5, 4],
        [5, 6, 7, 8, 16, 8, 7, 6, 5],
        [4, 5, 6, 7, 7, 7, 6, 5, 4],
        [3, 4, 5, 6, 6, 6, 5, 4, 3],
        [2, 3, 4, 5, 5, 5, 4, 3, 2],
        [1, 2, 3, 4, 4, 4, 3, 2, 1],
    ]
    board.assign_board_weights()
    assert board._board_weights == weights
