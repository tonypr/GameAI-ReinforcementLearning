import unittest
import sys

import main


class TestMain(unittest.TestCase):
    def test_configurations(self):
        config_file = "configurations/default.yml"
        for game in main.games:
            args = [
                'main.py', '-f', config_file, '-g', game, '-n', '2', '-p',
                False
            ]
            sys.argv = args
            main.main()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMain)
    unittest.TextTestRunner(verbosity=2).run(suite)
