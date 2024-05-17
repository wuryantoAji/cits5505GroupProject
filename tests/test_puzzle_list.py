import unittest
from flask import url_for
from flask_testing import TestCase
from application import create_app, db
from application.models import WordlePuzzle

class TestPuzzleList(TestCase):
    def create_app(self):
        app = create_app()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        return app

    def setUp(self):
        db.create_all()

        # Create test puzzles
        puzzle1 = WordlePuzzle(
            puzzle_name='Puzzle 1',
            puzzle_solution='TEST',
            number_of_attempt=3,
            puzzle_score=100,
            times_puzzle_played=0
        )
        puzzle2 = WordlePuzzle(
            puzzle_name='Puzzle 2',
            puzzle_solution='TEST',
            number_of_attempt=3,
            puzzle_score=100,
            times_puzzle_played=0
        )
        db.session.add_all([puzzle1, puzzle2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_puzzle_list_render(self):
        # Access the puzzle list page
        response = self.client.get('/puzzle-list/')
        
        # Check if the page renders successfully
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Puzzle 1', response.data)  # Check if puzzle names are in the response
        self.assertIn(b'Puzzle 2', response.data)

if __name__ == '__main__':
    unittest.main()
