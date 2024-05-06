from application import db
from application.models import User, WordlePuzzle
 
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