import random
from builtins import range

class QLearner(object):
    def __init__(self, actions, transition, reward, epsilon, alpha, gamma):
        self.actions = actions
        self.transition = transition
        self.reward = reward
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.Q = {}

    def getQ(self, q_pair):
        if q_pair not in self.Q:
            self.Q[q_pair] = 0
        return self.Q[q_pair]

    def bestQ(self, state):
        actions = self.actions(state)
        if len(actions) == 0:
            return 0, 0
        maxAction = random.choice(actions)
        maxQ = self.getQ((state, maxAction))

        for action in actions:
            q_pair = (state, action)
            curQ = self.getQ(q_pair)
            if curQ > maxQ:
                maxAction, maxQ = action, curQ
        return (maxAction, maxQ)

    def updateQ(self, state, action):
        new_state = self.transition(state, action)
        reward = self.reward(new_state, action)
        q_pair = (state, action)
        q_value = self.getQ(q_pair)
        q_update = reward - self.gamma * self.bestQ(new_state)[1] - q_value
        self.Q[q_pair] += self.alpha * q_update

    def exploreState(self, state):
        rand = random.random()
        if rand < self.epsilon:
            action = random.choice(self.actions(state))
        else:
            action = self.bestQ(state)[0]
        self.updateQ(state, action)
        return action

class QLearnerGameAI(QLearner):
    def __init__(self, game, epsilon, alpha, gamma):
        QLearner.__init__(self, game.actions, game.transition, game.reward, epsilon, alpha, gamma)
        self.game = game
        self.numGamesLearned = 0

    def learnedMove(self, state):
        move = self.bestQ(state)[0]
        return move

    def learnSteps(self, numSteps):
        state = self.game.startNewGame()
        for i in range(numSteps):
            action = self.exploreState(state)
            state = self.game.takeAction(action)
            if not self.game.isGameRunning:
                state = self.game.startNewGame()

    def learnGames(self, numGames):
        for i in range(numGames):
            state = self.game.startNewGame()

            while self.game.isGameRunning:
                action = self.exploreState(state)
                state = self.game.takeAction(action)

            self.numGamesLearned += 1
