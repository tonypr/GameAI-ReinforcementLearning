import random

class QLearner(object):
    def __init__(self, start_state, actions, transition, reward, epsilon, alpha, gamma):
        self.start_state = start_state
        self.actions = actions
        self.transition = transition
        self.reward = reward
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.state = start_state
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
        return reward


    def learn(self, state):
        rand = random.random()
        if rand < self.epsilon:
            action = random.choice(self.actions(state))
        else:
            action = self.bestQ(state)[0]
        reward = self.updateQ(state, action)
        new_state = self.transition(state, action)
        return action, new_state, reward

class QLearnerGameAI(QLearner):
    def __init__(self, game, epsilon, alpha, gamma):
        QLearner.__init__(self, game.start, game.actions, game.transition, game.reward, epsilon, alpha, gamma)
        self.numGamesLearned = 0

    def learnedMove(self, state):
        move = self.bestQ(state)[0]
        return move

    def learnSteps(self, numSteps):
        state = self.start_state
        for i in xrange(numSteps):
            action, state, reward = self.learn(state)
            win = abs(reward) == 1
            tie = len(self.actions(state)) == 0
            if tie or win:
                state = self.start_state

    def learnGames(self, numGames):
        for i in xrange(numGames):
            gameNotFinished = True
            state = self.start_state
            while gameNotFinished:
                action, state, reward = self.learn(state)
                win = abs(reward) == 1
                tie = len(self.actions(state)) == 0
                gameNotFinished = not (tie or win)
            self.numGamesLearned += 1
            if self.numGamesLearned > 50000 and self.epsilon > 0.25:
                self.epsilon = 0.2
            elif self.numGamesLearned > 100000 and self.epsilon == 0.2:
                self.epsilon = 0.1
