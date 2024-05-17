import unittest

# from test_auth import TestAuth
from . import test_auth
from . import test_login_register
from . import test_create_game
from . import test_play_game
from . import test_puzzle_list

if __name__ == '__main__':
    # Create a test suite
    suite = unittest.TestSuite()

    # Add test cases to the suite
    suite.addTest(unittest.makeSuite(test_auth))
    suite.addTest(unittest.makeSuite(test_login_register))
    suite.addTest(unittest.makeSuite(test_create_game))
    suite.addTest(unittest.makeSuite(test_play_game))
    suite.addTest(unittest.makeSuite(test_puzzle_list))

    # Initialize a test runner
    runner = unittest.TextTestRunner(verbosity=2)

    # Run the test suite
    result = runner.run(suite)
