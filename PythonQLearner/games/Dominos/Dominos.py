from GameSetup import Game
from Domino import Domino
from DominoState import DominoState

from os import path, makedirs

scriptPath = path.abspath(__file__)
scriptDir = path.split(scriptPath)[0]
AIsDirectory = path.join(scriptDir, "AIs/")

#
# State is a 8 element tuple of:
# - dominos remaining
# - current player's hand
# - player 1's plays
# - player 2's plays
# - player 3's plays
# - player 4's plays
# - left end domino
# - right end domino

class DominosGame(Game):
    def __init__(self):
        self.name = "Dominos"
        self.AIpath = AIsDirectory
        self.players = 4
        self.dominoState = DominoState()

    def startNewGame(self):
        self.isGameRunning = True
        self.state = self.dominoState.start()
        return self.state

    def takeAction(self, action):
        self.state = self.dominoState.doTransition(action)
        winner = self.checkGameOver(self.state, action)
        if winner != -1:
            self.isGameRunning = False
        return self.state

    def actions(self, state):
        return self.dominoState.actions()

    def transition(self, state, action):
        return self.dominoState.transition(action)

    def checkWin(self, state, player):
        return len(state[player + 1]) == 7

    def checkTie(self, state):
        return False

    def checkGameOver(self, state, prevMove):
        for player in xrange(1, self.players + 1):
            if self.checkWin(state, player):
                return player
        if self.checkTie(state):
            return 0
        return -1

    def reward(self, state, prevMove):
        winner = self.checkGameOver(state, prevMove)
        if winner > 0:
            return 1
        return 0

    def displayBoard(self, state):
        print(self.dominoState)

    def displayGameEnd(self, state):
        self.displayBoard(state)
        winner = self.checkGameOver(state, None)
        if winner == 0:
            print("It was a tie!")
        else:
            print("The winner was player " + str(winner) + "!")
