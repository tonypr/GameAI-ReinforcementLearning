from GameSetup import Game

from os import path, makedirs
from builtins import range

scriptPath = path.abspath(__file__)
scriptDir = path.split(scriptPath)[0]
AIsDirectory = path.join(scriptDir, "AIs/")

class Connect4Game(Game):
    def __init__(self):
        self.name = "Connect4"
        self.AIpath = AIsDirectory
        self.players = 2
        self.w = 7
        self.h = 6
        self.start = tuple([(0,)*self.h for i in range(self.w)])
        self.isGameRunning = False

    def startNewGame(self):
        self.isGameRunning = True
        self.state = self.start
        return self.state

    def takeAction(self, action):
        self.state = self.transition(self.state, action)
        winner = self.checkGameOver(self.state, action)
        if winner != -1:
            self.isGameRunning = False
        return self.state

    def actions(self, state):
        return [i+1 for i in range(self.w) if state[i][-1] == 0]

    def transition(self, state, action):
        column = action - 1
        player = (self.count_moves(state) % 2) + 1
        temp_state = list(state)
        temp_plays = list(state[column])
        play_location = temp_plays.index(0)
        temp_plays[play_location] = player
        temp_state[column] = tuple(temp_plays)
        return tuple(temp_state)

    def count_moves(self, state):
        moves = 0

        for column in state:
            for square in column:
                if square != 0:
                    moves += 1

        return moves

    def check_square(self, state, x, y):
        all_1 = (1,1,1,1)
        all_2 = (2,2,2,2)

        square_states = set()

        ## check possible wins
        for j in range(4):
            if x-j >= 0 and x-j+3 < self.w:
                horizontal_squares = tuple(state[x-j+i][y] for i in range(4))
                square_states.add(horizontal_squares)

                if y-j >= 0 and y-j+3 < self.h:
                    diag_up_squares = tuple(state[x-j+i][y-j+i] for i in range(4))
                    square_states.add(diag_up_squares)

                if y+j-3 >= 0 and y+j < self.h:
                    diag_down_squares = tuple(state[x-j+i][y+j-i] for i in range(4))
                    square_states.add(diag_down_squares)

            if y-j >= 0 and y-j+3 < self.h:
                vertical_squares = tuple(state[x][y-j+i] for i in range(4))
                square_states.add(vertical_squares)

        if all_1 in square_states:
            return 1
        elif all_2 in square_states:
            return 2
        else:
            return 0

    def checkTie(self, state):
        tie = True
        for i in range(self.w):
            if state[i][-1] == 0:
                tie = False
                break
        return tie

    def checkGameOver(self, state, prevMove):
        if prevMove is not None:
            column = prevMove - 1
            row = 0
            for ind, elem in enumerate(state[column]):
                if elem == 0:
                    row = ind - 1
                    break
            square_win = self.check_square(state, column, row)
            if square_win != 0:
                return square_win
        else:
            for i in range(self.w):
                for j in range(self.h):
                    square_win = self.check_square(state, i, j)
                    if square_win != 0:
                        return square_win

        if self.checkTie(state):
            return 0
        return -1

    def reward(self, state, prevMove):
        winner = self.checkGameOver(state, prevMove)
        if winner > 0:
            return 1
        return 0

    def row_board(self, state, h, w):
        row_list = ["|"]
        for i in range(w):
            square_i = state[i][h]
            square_str = " "
            if square_i != 0:
                square_str = str(square_i)
            row_list.append(square_str)
            row_list.append("|")
        row_list.append("\n")
        row_str = "".join(row_list)
        return row_str

    def bottom_board(self, w):
        row_list = [" "]
        for i in range(w):
            row_list.append(str(i+1))
            row_list.append(" ")
        row_list.append("\n")
        row_str = "".join(row_list)
        return row_str

    def displayBoard(self, state):
        h = len(state[0])
        w = len(state)

        board = "\n"

        horizontal_line = "-"*(2*w+1) + "\n"
        board += horizontal_line

        for i in range(h):
            row_from_top = self.row_board(state, h-i-1, w)
            board += row_from_top
            board += horizontal_line
        board += self.bottom_board(w)
        print(board)

    def displayGameEnd(self, state):
        self.displayBoard(state)
        winner = self.checkGameOver(state, None)
        if winner == 1:
            print("Player 1 won!")
        elif winner == 2:
            print("Player 2 won!")
        else:
            print("It was a tie!")
