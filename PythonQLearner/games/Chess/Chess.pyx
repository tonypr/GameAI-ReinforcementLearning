import chess

from GameSetup import Game


class ChessGame(Game):
    def __init__(self):
        self.name = "Chess"
        self.players = 2
        self.isGameRunning = False
        self.start = chess.Board().fen()

    def startNewGame(self):
        self.isGameRunning = True
        self.stateBoard = chess.Board()
        self.state = self.stateBoard.fen()
        return self.state

    def takeAction(self, action):
        self.stateBoard.push(action)
        self.state = self.stateBoard.fen()
        self.isGameRunning = not self.stateBoard.is_game_over()
        return self.state

    def actions(self, state):
        state = chess.Board(state)
        return list(state.legal_moves)

    def transition(self, state, action):
        state = chess.Board(state)
        state.push(action)
        return state.fen()

    def reward(self, state, action):
        state = chess.Board(state)
        if state.result() == '1-0' or state.result() == '0-1':
            return 1
        return 0

    def checkGameOver(self, state, move):
        state = chess.Board(state)
        if not state.is_game_over():
            return -1
        return 0

    def displayBoard(self, state):
        state = chess.Board(state)
        print(state)

    def displayGameEnd(self, state):
        self.displayBoard(state)
        state = chess.Board(state)
        winner = state.result()
        msg = {
            '1-0': 'White won!',
            '0-1': 'Black won!',
            '1/2-1/2': 'It was a tie!',
            '*': 'Oops! Game still in play'
        }
        print(msg[winner])
