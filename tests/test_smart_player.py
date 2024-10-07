import os

import yaml
from classes.game import Game
from classes.player import DumbPlayer, SmartPlayer

# import random


GAME_CONFIG_PATH = "../config/game.yml"

with open(os.path.join(os.path.dirname(__file__), GAME_CONFIG_PATH), "r") as file:
    game_config = yaml.safe_load(file)

for config_name, path in game_config["config_paths"].items():
    with open(path, "r") as file:
        game_config[config_name] = yaml.safe_load(file)
        board_config = game_config["board_config"]


def test_game_is_invisited_left():
    game = Game(game_config)
    game.board.player_black = DumbPlayer(stone_color="B")
    game.board.player_white = SmartPlayer(
        stone_color="W", opponent=game.board.player_black
    )
    game.board.current_player = game.board.player_black
    assert game.board.player_white.is_unvisited_left(game.board)


def test_game_isnot_invisited_left():
    game = Game(game_config)
    game.board.player_black = DumbPlayer(stone_color="B")
    game.board.player_white = SmartPlayer(
        stone_color="W", opponent=game.board.player_black
    )
    game.board.current_player = game.board.player_black
    assert not game.board.player_white.is_unvisited_left(game.board)


def test_game_evaluate_draw():
    game = Game(game_config)
    game.board.player_black = DumbPlayer(stone_color="B")
    game.board.player_white = SmartPlayer(
        stone_color="W", opponent=game.board.player_black
    )
    game.board.current_player = game.board.player_black
    assert game.board.player_white.evaluate(game.board) == 0


def test_game_evaluate_blackwin():
    game = Game(game_config)
    game.board.player_black = DumbPlayer(stone_color="B")
    game.board.player_white = SmartPlayer(
        stone_color="W", opponent=game.board.player_black
    )
    game.board.current_player = game.board.player_black
    assert game.board.player_white.evaluate(game.board) == 10


def test_game_evaluate_whitewin():
    game = Game(game_config)
    game.board.player_black = DumbPlayer(stone_color="B")
    game.board.player_white = SmartPlayer(
        stone_color="W", opponent=game.board.player_black
    )
    game.board.current_player = game.board.player_black
    assert game.board.player_white.evaluate(game.board) == -10


def test_game_minimax():
    game = Game(game_config)
    game.board.player_black = DumbPlayer(stone_color="B")
    game.board.player_white = SmartPlayer(
        stone_color="W", opponent=game.board.player_black
    )
    game.board.current_player = game.board.player_black
    assert game.minimax(game.board, 0, game.board.player_white) == 0
