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


@pytest.fixture
def empty_board():
    n = board_config["n_cells"]

    _board = []
    for i in range(n):
        _board.append([])
        for j in range(n):
            stone = Stone(x=i, y=j, color="_", visited=False)
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


def test_game_evaluate_draw(empty_board):
    game = Game(game_config)
    game.board.player_black = Player(stone_color="B")
    game.board.player_white = SmartPlayer(
        stone_color="W", opponent=game.board.player_black
    )
    game.board.current_player = game.board.player_black

    black_player_inputs = [(0, 0), (1, 0), (2, 0), (3, 0)]
    for x, y in black_player_inputs:
        empty_board[x][y].color = "B"
        empty_board[x][y].visited = True
        empty_board[x][y].player = game.board.player_black

    white_player_inputs = [(0, 1), (1, 1), (1, 2), (3, 1)]
    for x, y in white_player_inputs:
        empty_board[x][y].color = "W"
        empty_board[x][y].visited = True
        empty_board[x][y].player = game.board.player_white

    game.board.set_board(empty_board)

    assert game.board.player_white.evaluate(game.board, 0) == 0


def test_game_evaluate_blackwin(empty_board):
    game = Game(game_config)
    game.board.player_black = Player(stone_color="B")
    game.board.player_white = SmartPlayer(
        stone_color="W", opponent=game.board.player_black
    )
    game.board.current_player = game.board.player_black

    """
    scenario for n = 9 and n_win = 5:
    B W _ _ _ _ _ _ _
    B W W _ _ _ _ _ _
    B B _ _ _ _ _ _ _
    B W _ _ _ _ _ _ _
    B _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _
    """
    black_player_inputs = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)]
    for x, y in black_player_inputs:
        empty_board[x][y].color = "B"
        empty_board[x][y].visited = True
        empty_board[x][y].player = game.board.player_black

    white_player_inputs = [(0, 1), (1, 1), (1, 2), (3, 1)]
    for x, y in white_player_inputs:
        empty_board[x][y].color = "W"
        empty_board[x][y].visited = True
        empty_board[x][y].player = game.board.player_white

    game.board.set_board(empty_board)

    assert game.board.player_white.evaluate(game.board, 0) == -5


def test_game_evaluate_whitewin(empty_board):
    game = Game(game_config)
    game.board.player_black = Player(stone_color="B")
    game.board.player_white = SmartPlayer(
        stone_color="W", opponent=game.board.player_black
    )
    game.board.current_player = game.board.player_white

    """
    scenario for n = 9 and n_win = 5:
    B W _ _ _ _ _ _ _
    B W W _ _ _ _ _ _
    B B B W _ _ _ _ _
    W W B B W _ _ _ _
    _ _ _ _ B W _ _ _
    _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _
    """
    black_player_inputs = [
        (0, 0),
        (1, 0),
        (2, 0),
        (2, 1),
        (2, 2),
        (3, 2),
        (3, 3),
        (4, 4),
    ]
    for x, y in black_player_inputs:
        empty_board[x][y].color = "B"
        empty_board[x][y].visited = True
        empty_board[x][y].player = game.board.player_black

    white_player_inputs = [
        (0, 1),
        (0, 3),
        (1, 1),
        (1, 2),
        (2, 3),
        (3, 1),
        (3, 4),
        (4, 5),
    ]
    for x, y in white_player_inputs:
        empty_board[x][y].color = "W"
        empty_board[x][y].visited = True
        empty_board[x][y].player = game.board.player_white

    game.board.set_board(empty_board)

    assert game.board.player_white.evaluate(game.board, 0) == 5


def test_game_find_optimal_move(empty_board):
    game = Game(game_config)
    game.board.player_black = Player(stone_color="B")
    game.board.player_white = SmartPlayer(
        stone_color="W", opponent=game.board.player_black
    )
    game.board.current_player = game.board.player_white

    """
    scenario for n = 9 and n_win = 5:
    B W _ _ _ _ _ _ _
    B W W _ _ _ _ _ _
    B B _ _ _ _ _ _ _
    B W _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _
    _ _ _ _ _ _ _ _ _
    """

    black_player_inputs = [(0, 0), (1, 0), (2, 0), (3, 0)]
    for x, y in black_player_inputs:
        empty_board[x][y].color = "B"
        empty_board[x][y].visited = True
        empty_board[x][y].player = game.board.player_black

    white_player_inputs = [(0, 1), (1, 1), (1, 2), (3, 1)]
    for x, y in white_player_inputs:
        empty_board[x][y].color = "W"
        empty_board[x][y].visited = True
        empty_board[x][y].player = game.board.player_white

    game.board.set_board(empty_board)

    smart_player_input = game.board.player_white.get_input(game.board)
    x, y = game.validate_input(smart_player_input)
    assert (x, y) == (4, 0)  # win condition for white player
