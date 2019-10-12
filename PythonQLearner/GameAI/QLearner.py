import random
from builtins import range
from collections import defaultdict


class QLearner(object):
    def __init__(self, actions, transition, reward, epsilon, alpha, gamma):
        self.actions = actions
        self.transition = transition
        self.reward = reward
        self.epsilon = epsilon
        self.alpha = alpha
        self.gamma = gamma
        self.Q = defaultdict(int)

    def best_q(self, state):
        actions = self.actions(state)
        
        if len(actions) == 0:
            return 0, 0

        maxAction = random.choice(actions)
        maxQ = self.Q[(state, maxAction)]

        for action in actions:
            q_pair = (state, action)
            curQ = self.Q[q_pair]
            if curQ > maxQ:
                maxAction, maxQ = action, curQ
        return (maxAction, maxQ)

    def update_q(self, state, action):
        new_state = self.transition(state, action)
        reward = self.reward(new_state, action)
        q_pair = (state, action)
        q_value = self.Q[q_pair]
        q_update = reward - self.gamma * self.best_q(new_state)[1] - q_value
        self.Q[q_pair] += self.alpha * q_update

    def explore_state(self, state):
        rand = random.random()
        if rand < self.epsilon:
            action = random.choice(self.actions(state))
        else:
            action = self.best_q(state)[0]
        self.update_q(state, action)
        return action


class QLearnerGameAI(QLearner):
    def __init__(self, game, epsilon, alpha, gamma):
        QLearner.__init__(self, game.actions, game.transition, game.reward,
                          epsilon, alpha, gamma)
        self.game = game
        self.numGamesLearned = 0

    def learnedMove(self, state):
        move = self.best_q(state)[0]
        return move

    def learnSteps(self, num_steps):
        state = self.game.startNewGame()
        for i in range(num_steps):
            action = self.explore_state(state)
            state = self.game.takeAction(action)
            if not self.game.isGameRunning:
                state = self.game.startNewGame()

    def learnGames(self, num_games):
        for i in range(num_games):
            state = self.game.startNewGame()

            while self.game.isGameRunning:
                action = self.explore_state(state)
                state = self.game.takeAction(action)

            self.numGamesLearned += 1
