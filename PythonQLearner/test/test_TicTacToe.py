from games.TicTacToe import TicTacToeGame
import unittest

class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.TicTacToe = TicTacToeGame()
        self.state = self.TicTacToe.startNewGame()

class TicTacToeBasic(BaseTestCase):
    def test_start(self):
        self.assertEqual(self.state, ((), ()))

    def test_valid_moves(self):
        move = 1
        self.state = self.TicTacToe.takeAction(move)
        self.assertEqual(self.state, ((1,), ()))

        move = 2
        self.state = self.TicTacToe.takeAction(move)
        self.assertEqual(self.state, ((1,), (2,)))

    def test_invalid_moves(self):
        move = 1
        self.state = self.TicTacToe.takeAction(move)
        self.assertEqual(self.state, ((1,), ()))

        move = 1
        with self.assertRaises(AssertionError):
            self.state = self.TicTacToe.takeAction(move)

        move = "1"
        with self.assertRaises(AssertionError):
            self.state = self.TicTacToe.takeAction(move)

if __name__ == '__main__':
    unittest.main()
