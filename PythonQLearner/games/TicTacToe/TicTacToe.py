from GameSetup import Game
from builtins import range
from os import path, makedirs

scriptPath = path.abspath(__file__)
scriptDir = path.split(scriptPath)[0]
AIsDirectory = path.join(scriptDir, "AIs/")


class TicTacToeGame(Game):
    def __init__(self):
        self.name = "TicTacToe"
        self.AIpath = AIsDirectory
        self.players = 2
        self.start = ((), ())
        self.isGameRunning = False

    def startNewGame(self):
        self.isGameRunning = True
        self.state = self.start
        return self.state

    def takeAction(self, action):
        assert action in self.actions(self.state)
        self.state = self.transition(self.state, action)
        winner = self.checkGameOver(self.state, action)
        if winner != -1:
            self.isGameRunning = False
        return self.state

    def actions(self, state):
        return [
            i for i in range(1, 10)
            if (i not in state[0] and i not in state[1])
        ]

    def transition(self, state, action):
        assert action in self.actions(state)
        turn = (len(state[0]) + len(state[1])) % 2
        temp_state = list(state)
        temp_plays = list(state[turn])
        temp_plays.append(action)
        temp_state[turn] = tuple(temp_plays)
        return tuple(temp_state)

    def checkWin(self, state, player):
        plays = state[player - 1]
        wins = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8),
                (3, 6, 9), (1, 5, 9), (3, 5, 7)]
        won = False
        for win in wins:
            win_check = True
            for num in win:
                if num not in plays:
                    win_check = False
                    break
            if win_check:
                won = True
                break
        return won

    def checkTie(self, state):
        return len(state[0]) + len(state[1]) == 9

    def checkGameOver(self, state, prevMove):
        for player in range(1, self.players + 1):
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

    def getBoard(self, state):
        board = [" " for i in range(9)]

        x = state[0]
        circle = state[1]

        for play in x:
            board[play - 1] = "X"

        for play in circle:
            board[play - 1] = "O"

        return board

    def displayBoard(self, state):
        board = self.getBoard(state)
        print("\n=======================\n")
        print('   |   |')
        print(' ' + board[0] + ' | ' + board[1] + ' | ' + board[2])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[3] + ' | ' + board[4] + ' | ' + board[5])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[6] + ' | ' + board[7] + ' | ' + board[8])
        print('   |   |')

    def displayGameEnd(self, state):
        self.displayBoard(state)
        winner = self.checkGameOver(state, None)
        if winner == 1:
            print("X won!")
        elif winner == 2:
            print("O won!")
        else:
            print("It was a tie!")
