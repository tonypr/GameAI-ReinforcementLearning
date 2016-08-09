from games.Dominos import DominosGame
from GameSetup import HumanPlayer, AI
import time

## Set up game
Dominos = DominosGame()
human = HumanPlayer(Dominos)

## Set up AI players
epsilon = 0.3
alpha = 0.9
gamma = 0.9

DominosAI = AI(Dominos, epsilon, alpha, gamma)

numGames = 10
DominosAI.learnGames(numGames)

players = [human, DominosAI, DominosAI, DominosAI]
while True:
    Dominos.playGame(players)
    time.sleep(2)
    print("\n\n\n")
