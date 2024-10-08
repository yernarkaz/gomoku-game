import os

import pytest
import random
import yaml
from classes.game import Game
from classes.player import Player, SmartPlayer
from classes.stone import Stone

GAME_CONFIG_PATH = "../config/game.yml"

with open(os.path.join(os.path.dirname(__file__), GAME_CONFIG_PATH), "r") as file:
    game_config = yaml.safe_load(file)

for config_name, path in game_config["config_paths"].items():
    with open(path, "r") as file:
        game_config[config_name] = yaml.safe_load(file)
        board_config = game_config["board_config"]


@pytest.fixture
def random_full_board():
    random.seed(42)
    n = board_config["n_cells"]

    colors = ["B", "W"]
    _board = []
    for i in range(n):
        _board.append([])
        for j in range(n):
            c_ind = random.randint(0, 1)
            c = colors[c_ind]
            stone = Stone(x=i, y=j, color=c, visited=True)
            _board[i].append(stone)

    return _board


@pytest.fixture
def random_scenario_board():
    random.seed(42)
    n = board_config["n_cells"]

    colors = ["B", "W", "_"]
    _board = []
    for i in range(n):
        _board.append([])
        for j in range(n):
            c_ind = random.randint(0, 2)
            c = colors[c_ind]
            stone = Stone(x=i, y=j, color=c, visited=True if c != "_" else False)
            _board[i].append(stone)

    return _board


def test_game_is_invisited_left():
    game = Game(game_config)
    game.board.player_black = Player(stone_color="B")
    game.board.player_white = SmartPlayer(
        stone_color="W", opponent=game.board.player_black
    )
    game.board.current_player = game.board.player_black
    assert game.board.player_white.is_unvisited_left(game.board)


def test_game_isnot_invisited_left(random_full_board):
    game = Game(game_config)
    game.board.player_black = Player(stone_color="B")
    game.board.player_white = SmartPlayer(
        stone_color="W", opponent=game.board.player_black
    )
    game.board.current_player = game.board.player_black
    game.board.set_board(random_full_board)

    assert not game.board.player_white.is_unvisited_left(game.board)


def test_game_evaluate_draw(random_scenario_board):
    game = Game(game_config)
    game.board.player_black = Player(stone_color="B")
    game.board.player_white = SmartPlayer(
        stone_color="W", opponent=game.board.player_black
    )
    game.board.current_player = game.board.player_black
    game.board.set_board(random_scenario_board)

    assert game.board.player_white.evaluate(game.board, 0) == 0


def test_game_evaluate_blackwin(random_scenario_board):
    game = Game(game_config)
    game.board.player_black = Player(stone_color="B")
    game.board.player_white = SmartPlayer(
        stone_color="W", opponent=game.board.player_black
    )
    game.board.current_player = game.board.player_black

    for j in range(game.board.get_nwin()):
        random_scenario_board[0][j].color = "B"
        random_scenario_board[0][j].visited = True
        random_scenario_board[0][j].player = game.board.player_black

    game.board.set_board(random_scenario_board)

    assert game.board.player_white.evaluate(game.board, 0) == -10


def test_game_evaluate_whitewin(random_scenario_board):
    game = Game(game_config)
    game.board.player_black = Player(stone_color="B")
    game.board.player_white = SmartPlayer(
        stone_color="W", opponent=game.board.player_black
    )
    game.board.current_player = game.board.player_white

    for j in range(game.board.get_nwin()):
        random_scenario_board[0][j].color = "W"
        random_scenario_board[0][j].visited = True
        random_scenario_board[0][j].player = game.board.player_white

    game.board.set_board(random_scenario_board)
    print(game.board)

    assert game.board.player_white.evaluate(game.board, 0) == 10


# def test_game_minimax_for_black(random_scenario_board):
#     game = Game(game_config)
#     game.board.player_black = Player(stone_color="B")
#     game.board.player_white = SmartPlayer(
#         stone_color="W", opponent=game.board.player_black
#     )
#     game.board.current_player = game.board.player_black
#     game.board.set_board(random_scenario_board)

#     assert (
#         game.board.player_white.minimax(game.board, 0, game.board.current_player) == 10
#     )


# def test_game_minimax_for_white(random_scenario_board):
#     game = Game(game_config)
#     game.board.player_black = Player(stone_color="B")
#     game.board.player_white = SmartPlayer(
#         stone_color="W", opponent=game.board.player_black
#     )
#     game.board.current_player = game.board.player_white
#     game.board.set_board(random_scenario_board)

#     assert (
#         game.board.player_white.minimax(game.board, 0, game.board.current_player) == -10
#     )


# def test_game_find_optimal_move(random_scenario_board):
#     game = Game(game_config)
#     game.board.player_black = Player(stone_color="B")
#     game.board.player_white = SmartPlayer(
#         stone_color="W", opponent=game.board.player_black
#     )
#     game.board.current_player = game.board.player_white
#     game.board.set_board(random_scenario_board)

#     smart_player_input = game.board.player_white.get_input(game.board)
#     x, y = game.validate_input(smart_player_input)
#     assert (x, y) == (0, 0)
