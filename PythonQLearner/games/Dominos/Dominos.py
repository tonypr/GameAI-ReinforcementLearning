from GameSetup import Game
import collections
from Domino import Domino

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
        self.turn = 0

        dominos = [Domino(i, j) for i in range(7) for j in range(i, 7)]
        random.shuffle(dominos)
        self.hands = dominos[0:7], dominos[7:14], dominos[14:21], dominos[21:28]

    def actions(self, state):
        cur_hand = state[1]
        left_end = state[6]
        right_end = state[7]

        moves = []
        equal_ends = left_end == right_end
        for domino in cur_hand:
            if left_end in domino:
                moves.append((domino, 'LEFT'))
            if right_end in domino and not equal_ends:
                moves.append((domino, 'RIGHT'))
        return moves

    def transition(self, state, action):
        move_domino = action[0]
        dominos_remaining = list(state[0])
        dominos_remaining.remove(move_domino)
        

    def checkWin(self, state, player):

    def checkTie(self, state):

    def checkGameOver(self, state, prevMove):

    def reward(self, state, prevMove):
        winner = self.checkGameOver(state, prevMove)
        if winner > 0:
            return 1
        return 0
