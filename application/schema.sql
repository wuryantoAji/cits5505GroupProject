CREATE TABLE IF NOT EXISTS User (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    user_password TEXT,
    overall_score INTEGER
);

CREATE TABLE IF NOT EXISTS WordlePuzzle (
    puzzle_id INTEGER PRIMARY KEY,
    submitter_id INTEGER,
    puzzle_name TEXT,
    puzzle_solution TEXT,
    number_of_attempt INTEGER,
    puzzle_score INTEGER,
    FOREIGN KEY (submitter_id) REFERENCES User(user_id)
);

CREATE TABLE IF NOT EXISTS ScoreTable (
    score_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    puzzle_id INTEGER,
    score_achieved INTEGER,
    FOREIGN KEY (user_id) REFERENCES User(user_id),
    FOREIGN KEY (puzzle_id) REFERENCES WordlePuzzle(puzzle_id)
);

-- Create the third table
CREATE TABLE IF NOT EXISTS Comments (
    comments_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    comment_text TEXT,
    posted_date TEXT,
    FOREIGN KEY (user_id) REFERENCES User(user_id)
);