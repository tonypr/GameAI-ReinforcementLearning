import random
from Domino import Domino

class DominoState(object):
    def __init__(self):
        dominos = [Domino(i, j) for i in range(7) for j in range(i, 7)]
        random.shuffle(dominos)
        self.hands = dominos[0:7], dominos[7:14], dominos[14:21], dominos[21:28]
    def getQlearningState(self):
