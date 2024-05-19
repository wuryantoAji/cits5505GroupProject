import unittest

# from test_auth import TestAuth
from . import test_login_register
from . import test_create_game
from . import test_play_game
from . import test_puzzle_list
from . import test_leaderboard
from . import test_profile



# Create a test suite
suite = unittest.TestSuite()

# Add test cases to the suite
suite.addTest(unittest.makeSuite(test_login_register.TestAuth))
suite.addTest(unittest.makeSuite(test_create_game.TestCreateGame))
suite.addTest(unittest.makeSuite(test_play_game.TestPlayGame))
suite.addTest(unittest.makeSuite(test_puzzle_list.TestPuzzleList))
suite.addTest(unittest.makeSuite(test_leaderboard.TestLeaderboard))
suite.addTest(unittest.makeSuite(test_profile.TestProfile))

# Initialize a test runner
runner = unittest.TextTestRunner(verbosity=2)

# Run the test suite
result = runner.run(suite)
