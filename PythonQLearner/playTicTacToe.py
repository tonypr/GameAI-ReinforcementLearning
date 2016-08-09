from games.TicTacToe import TicTacToeGame
from GameSetup import HumanPlayer, AI
import time

## Set up game
TicTacToe = TicTacToeGame()
human = HumanPlayer(TicTacToe)

## Set up AI players
epsilon = 0.3
alpha = 0.9
gamma = 0.9

TicTacToeAI = AI(TicTacToe, epsilon, alpha, gamma)

numGames = 100000
TicTacToeAI.learnGames(numGames)

players = [human, TicTacToeAI]
while True:
    TicTacToe.playGame(players)
    time.sleep(2)
    print("\n\n\n")
