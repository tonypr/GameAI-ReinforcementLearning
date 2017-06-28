import argparse
import yaml
import sys
import time

from games import *
from GameSetup import *

__author__ = "Anthony Erb Lugo"


def update_settings(settings, config_file):
    with open(config_file, 'r') as config_file_input:
        config_settings = yaml.load(config_file_input)
        settings.update(config_settings)


def parse_arguments():
    settings = {}
    update_settings(settings, "configurations/default.yml")

    parser = argparse.ArgumentParser(description="Run game AI learner")
    parser.add_argument(
        "-f",
        "--configuration_file",
        type=str,
        required=False,
        help="YAML configuration file. E.g. "
        "configurations/tictactoe.yml")
    parser.add_argument(
        "-g",
        "--game",
        type=str,
        required=False,
        help="Game to run. E.g. TicTacToe")
    parser.add_argument(
        "-n",
        "--num_games",
        type=str,
        required=False,
        help="Number of games to train. E.g. 1000")
    parser.add_argument(
        "-p", "--play", type=str, required=False, help="Play game", default="False", choices=["True", "False"])
    parser.add_argument(
        "-p1",
        "--player_1",
        type=str,
        required=False,
        help="Player one type. E.g. Human, Random")
    parser.add_argument(
        "-p2",
        "--player_2",
        type=str,
        required=False,
        help="Player two type. E.g. Human, Random")
    parser.add_argument(
        "-e", "--epsilon", type=float, required=False, help="Epsilon.")
    parser.add_argument(
        "-a", "--alpha", type=float, required=False, help="Alpha.")
    parser.add_argument("--gamma", type=float, required=False, help="Gamma.")
    _args = vars(parser.parse_args())
    print(_args)

    # Read configuration file
    if _args['configuration_file'] is not None:
        update_settings(settings, _args["configuration_file"])

    settings.update((k, v) for k, v in _args.items() if v is not None)

    if _args["play"] is not None:
        settings["play"] = _args["play"] == "True"

    players = [settings["player_1"], settings["player_2"]]

    settings['game'] = games[settings['game']]
    settings['num_games'] = conv_num_games(settings['num_games'])
    settings['players'] = [players_map[player] for player in players]
    print(settings)
    return settings


def main():
    settings = parse_arguments()

    game = settings['game']()
    human = HumanPlayer(game)
    gameAI = AI(game, settings['epsilon'], settings['alpha'],
                settings['gamma'])

    gameAI.learnGames(settings['num_games'])

    if settings['play']:
        players = [human, gameAI]
        while True:
            winner = game.playGame(players)
            time.sleep(2)
            print("\n\n\n")


if __name__ == '__main__':
    main()
