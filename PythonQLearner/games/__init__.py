from __future__ import absolute_import

from games.TicTacToe.TicTacToe import TicTacToeGame
from games.Connect4.Connect4 import Connect4Game
# from games.Chess.Chess import ChessGame

games = {
    "TicTacToe": TicTacToeGame,
    "Connect4": Connect4Game,
    # "Chess": ChessGame
}

num_games = {"short": 10000, "medium": 100000, "long": 500000}


def conv_num_games(input_games):
    if input_games in num_games:
        return num_games[input_games]
    return int(input_games)
