import unittest
import sys
import os

import main

def dir_explore(directory):
    for path in os.listdir(directory):
        full_path = os.path.join(directory, path)
        if os.path.isdir(full_path):
            continue
        yield full_path

class TestMain(unittest.TestCase):
    def test_configuration_default(self):
        config_file = "configurations/default.yml"
        for game in main.games:
            args = [
                'main.py', '-f', config_file, '-g', game, '-n', '2', '-p',
                False
            ]
            sys.argv = args
            main.main()

    def test_configurations(self):
        for config_file in dir_explore("configurations"):
            args = [
                'main.py', '-f', config_file, '-n', '2', '-p', False
            ]
            sys.argv = args
            main.main()

    def test_tictactoe_medium(self):
        config_file = "configurations/tictactoe.yml"
        args = [
            'main.py', '-f', config_file, '-n', 'medium', '-p',
            False
        ]
        sys.argv = args
        main.main()


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestMain)
    unittest.TextTestRunner(verbosity=2).run(suite)
