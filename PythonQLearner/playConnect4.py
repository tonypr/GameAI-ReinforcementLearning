from games.Connect4 import Connect4Game
from GameSetup import HumanPlayer, AI
import time

## Set up game
Connect4 = Connect4Game()
human = HumanPlayer(Connect4)

## Set up AI players
epsilon = 0.3
alpha = 0.9
gamma = 0.9

Connect4AI = AI(Connect4, epsilon, alpha, gamma)

numGames = 100000
Connect4AI.learnGames(numGames)

players = [human, Connect4AI]
while True:
    Connect4.playGame(players)
    time.sleep(2)
    print("\n\n\n")
