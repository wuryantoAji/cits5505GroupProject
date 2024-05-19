from application import db
from application.models import User, WordlePuzzle

WordlePuzzle.query.filter_by(user_id=1, puzzle_name="test10").delete()
db.session.commit()
 
u = User(username="admin",
         email="admin",
         password_hash="admin",
         overall_score=0)
db.session.add(u)
db.session.commit()
 
wp = WordlePuzzle(user_id=1,
         puzzle_name="test",
         puzzle_solution="catastrophe",
         number_of_attempt=10,
         puzzle_score=0,
         times_puzzle_played=0)
db.session.add(wp)
db.session.commit()

wp = WordlePuzzle(user_id=1,
         puzzle_name="test2",
         puzzle_solution="apples",
         number_of_attempt=10,
         puzzle_score=0,
         times_puzzle_played=0)
db.session.add(wp)
db.session.commit()

wp = WordlePuzzle(user_id=1,
         puzzle_name="test10",
         puzzle_solution="apples",
         number_of_attempt=10,
         puzzle_score=0,
         times_puzzle_played=0)
db.session.add(wp)
db.session.commit()