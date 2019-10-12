from GameAI.QLearner import QLearnerGameAI
import pickle
from os import path, makedirs
import time
import random
from builtins import input


def ensureDir(f):
    d = path.dirname(f)
    if not path.exists(d):
        makedirs(d)


class Game(object):
    def playGame(self, players):
        state = self.start
        turn = 0

        move = None
        while self.checkGameOver(state, move) == -1:
            self.displayBoard(state)
            player = players[turn % len(players)]
            move = player.play(state)
            state = self.transition(state, move)
            turn += 1
        self.displayGameEnd(state)
        return self.checkGameOver(state, move)


class HumanPlayer(object):
    def __init__(self, game):
        self.game = game

    def play(self, state):
        actions = [a for a in self.game.actions(state)]
        while True:
            print("Available moves: \n")
            for ind, action in enumerate(actions):
                print("{}: {}".format(ind + 1, str(action)))

            index = input("Please pick one of the available moves: ")
            index = int(index)
            if index < 1 or index > len(actions):
                print("That move is not available. Try again!")
            else:
                return actions[index - 1]


class RandomPlayer(object):
    def __init__(self, game):
        self.game = game

    def play(self, state):
        actions = self.game.actions(state)
        time.sleep(1)
        return random.choice(actions)


class AI(object):
    def __init__(self, game, epsilon, alpha, gamma):
        self.game = game
        self.gameAI = QLearnerGameAI(game, epsilon, alpha, gamma)

    def learnSteps(self, numSteps):
        self.gameAI.learnSteps(numSteps)

    def learnGames(self, numGames):
        self.gameAI.learnGames(numGames)

    def play(self, state):
        time.sleep(1)
        return self.gameAI.learnedMove(state)

    def getAIFilePath(self, name):
        gamePath = self.game.AIpath
        fileName = name + ".p"
        filePath = path.join(gamePath, fileName)
        ensureDir(gamePath)
        return filePath

    def saveAI(self, name):
        filePath = self.getAIFilePath(name)
        AI_info = (self.gameAI.Q, self.gameAI.num_games_learned)
        pickle.dump(AI_info, open(filePath, "wb"))

    def loadAI(self, name):
        filePath = self.getAIFilePath(name)
        try:
            self.gameAI.Q, self.gameAI.num_games_learned = pickle.load(
                open(filePath, "rb"))
        except IOError:
            print("Error: couldn't find AI file - skipped loading AI.")


players_map = {"Human": HumanPlayer, "Random": RandomPlayer, "AI": AI}
