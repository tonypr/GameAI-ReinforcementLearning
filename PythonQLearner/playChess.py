from games.Chess import ChessGame
from GameSetup import HumanPlayer, AI
import time

## Set up game
Chess = ChessGame()
human = HumanPlayer(Chess)

## Set up AI players
epsilon = 0.3
alpha = 0.9
gamma = 0.9

ChessAI = AI(Chess, epsilon, alpha, gamma)

numGames = 100
ChessAI.learnGames(numGames)

# players = [human, ChessAI]
# while True:
#     winner = Chess.playGame(players)
#     time.sleep(2)
#     print("\n\n\n")
