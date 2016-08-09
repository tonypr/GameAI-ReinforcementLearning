from GameAI.QLearner import QLearnerGameAI
import cPickle as pickle
from os import path, makedirs
import time

def ensureDir(f):
    d = path.dirname(f)
    if not path.exists(d):
        makedirs(d)

class Game(object):
    def playGame(self, players):
        state = self.startNewGame()
        turn = 0

        move = None
        while self.isGameRunning:
            self.displayBoard(state)
            player = players[turn % len(players)]
            move = player.play(state)
            state = self.takeAction(move)
            turn += 1
        self.displayGameEnd(state)

class HumanPlayer(object):
    def __init__(self, game):
        self.game = game

    def play(self, state):
        cur_hand = [str(a) for a in state[1]]
        print("Current hand: " + ", ".join(cur_hand))
        actions = [str(a) for a in self.game.actions(state)]
        while True:
            print("Available moves: " + ", ".join(actions))
            action = raw_input("Please pick one of the available moves: ")
            action_ind = int(action)
            if action_ind <= len(actions):
                return self.game.actions(state)[action_ind - 1]
            else:
                print("That move is not available. Try again!")

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
        AI_info = (self.gameAI.Q, self.gameAI.numGamesLearned)
        pickle.dump(AI_info, open(filePath, "wb"))

    def loadAI(self, name):
        filePath = self.getAIFilePath(name)
        try:
            self.gameAI.Q, self.gameAI.numGamesLearned = pickle.load(open(filePath, "rb"))
        except IOError:
            print "Error: couldn't find AI file - skipped loading AI."
