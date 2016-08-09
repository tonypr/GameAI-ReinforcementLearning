import random
from Domino import Domino
import collections
import copy

class DominoState(object):
    def get_QLearning_state(self):
        unplayed = frozenset(self.unplayed)
        cur_hand = tuple(self.hands[self.turn])
        left = self.left_end()
        right = self.right_end()
        state = [unplayed, cur_hand]
        for i in range(4):
            state.append(tuple(self.played[i]))
        state.append(left)
        state.append(right)
        return tuple(state)

    def get_QLearning(self, unplayed_, cur_hand_, played, left, right):
        unplayed = frozenset(unplayed_)
        cur_hand = tuple(cur_hand_)
        state = [unplayed, cur_hand]
        for i in range(4):
            state.append(tuple(played[i]))
        state.append(left)
        state.append(right)
        return tuple(state)

    def start(self):
        dominos = [Domino(i, j) for i in range(7) for j in range(i, 7)]
        random.shuffle(dominos)
        self.unplayed = set(dominos)
        self.hands = dominos[0:7], dominos[7:14], dominos[14:21], dominos[21:28]
        self.turn = 0
        self.played = [], [], [], []
        self.board = collections.deque()
        return self.get_QLearning_state()

    def transition(self, action):
        domino, left_or_right = action

        hands = copy.deepcopy(self.hands)
        played = copy.deepcopy(self.played)
        unplayed = self.unplayed.copy()

        if domino == Domino(-1, -1):
            played[self.turn].append(domino)
            cur_hand = hands[self.turn]
            left = self.left_end()
            right = self.right_end()
            return self.get_QLearning(unplayed, cur_hand, played, left, right)

        if domino not in hands[self.turn]:
            raise Exception('Cannot make move - {0} is not'
                            ' in the hand of player {1}.'.format(domino, self.turn))

        if left_or_right == 'LEFT':
            self.add_left(domino)
        elif left_or_right == 'RIGHT':
            self.add_right(domino)
        else:
            raise Exception('Cannot make move - `left_or_right` must be "LEFT" or "RIGHT".')

        hands[self.turn].remove(domino)
        played[self.turn].append(domino)
        unplayed.remove(domino)
        cur_hand = hands[self.turn]
        left = self.left_end()
        right = self.right_end()
        return self.get_QLearning(unplayed, cur_hand, played, left, right)

    def doTransition(self, action):
        domino, left_or_right = action
        if domino == Domino(-1, -1):
            self.played[self.turn].append(domino)
            self.turn = (self.turn + 1) % 4
            return self.get_QLearning_state()

        if domino not in self.hands[self.turn]:
            raise Exception('Cannot make move - {0} is not'
                            ' in the hand of player {1}.'.format(domino, self.turn))

        if left_or_right == 'LEFT':
            self.add_left(domino)
        elif left_or_right == 'RIGHT':
            self.add_right(domino)
        else:
            raise Exception('Cannot make move - `left_or_right` must be "LEFT" or "RIGHT".')

        self.hands[self.turn].remove(domino)
        self.played[self.turn].append(domino)
        self.unplayed.remove(domino)
        self.turn = (self.turn + 1) % 4
        return self.get_QLearning_state()

    def actions(self):
        if not self.board:
            return [(domino, 'LEFT') for domino in self.hands[self.turn]]

        moves = []

        left_end, right_end = self.ends()
        equal_ends = left_end == right_end
        for domino in self.hands[self.turn]:
            if left_end in domino:
                moves.append((domino, 'LEFT'))
            if right_end in domino and not equal_ends:
                moves.append((domino, 'RIGHT'))
        if len(moves) == 0:
            moves.append((Domino(-1, -1), 'LEFT'))

        return moves

    def left_end(self):
        if len(self.board) == 0:
            return None
        return self.board[0].first

    def right_end(self):
        if len(self.board) == 0:
            return None
        return self.board[-1].second

    def ends(self):
        return self.left_end(), self.right_end()

    def add_left(self, domino):
        if not self.board or domino.second == self.left_end():
            self.board.appendleft(domino)
        elif domino.first == self.left_end():
            self.board.appendleft(domino.inverted())
        else:
            raise Exception('{0} cannot be added to the left of'
                            ' the board - numbers do not match!'.format(domino))

    def add_right(self, domino):
        if not self.board or domino.first == self.right_end():
            self.board.append(domino)
        elif domino.second == self.right_end():
            self.board.append(domino.inverted())
        else:
            raise Exception('{0} cannot be added to the right of'
                            ' the board - numbers do not match!'.format(domino))

    def __len__(self):
        return len(self.board)

    def __str__(self):
        return ''.join([str(domino) for domino in self.board])
