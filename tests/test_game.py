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


def test_game_for_dumb_computer():
    game = Game(game_config)

    game.board.player_black = DumbPlayer(stone_color="B")
    game.board.player_white = DumbPlayer(stone_color="W")
    game.board.current_player = game.board.player_black

    while game.board.get_left_stones() > 0:
        print(f"{game.board.current_player.get_color_desc()} turn")

        xy_pairs = game.board.get_unvisited_xy_pairs()
        print(f"xy pairs left {game.board.get_left_stones()}:", xy_pairs)
        line_input = game.board.current_player.get_input(xy_pairs)
        print(f"Input: {line_input}")
        x, y = game.validate_input(line_input)

        if game.handle_turn(x, y):
            assert True

        print()
        print("-----------------------")
        print(game.board)
        print("-----------------------")
        print()

    assert True


def test_game_for_smart_computer():
    game = Game(game_config)

    game.board.player_black = DumbPlayer(stone_color="B")
    game.board.player_white = SmartPlayer(
        stone_color="W", opponent=game.board.player_black
    )
    game.board.current_player = game.board.player_black

    # while game.board.get_left_stones() > 0:
    #     print(f"{game.board.current_player.get_color_desc()} turn")

    #     if type(game.board.current_player) is DumbPlayer:
    #         xy_pairs = game.board.get_unvisited_xy_pairs()
    #         line_input = game.board.current_player.get_input(xy_pairs)
    #     elif type(game.board.current_player) is SmartPlayer:
    #         line_input = game.board.current_player.get_input(game.board)
    #     print(f"Input: {line_input}")
    #     x, y = game.validate_input(line_input)

    #     if game.handle_turn(x, y):
    #         assert True

    #     print()
    #     print("-----------------------")
    #     print(game.board)
    #     print("-----------------------")
    #     print()

    assert True
