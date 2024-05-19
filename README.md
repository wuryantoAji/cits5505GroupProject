# CITS5505GroupProject
Group project for CITS5505 - Agile Web Development

## Application Purpose (Design and Use Explanation)

## Group Member
| UWA ID       |        Name            | Github Username |
|--------------|:----------------------:|----------------:|
|   23698749   |     Aji Wuryanto       |   wuryantoAji   |
|   23786945   |     Chuanrui Yang      |     dtdoris     |
|   22609525   | Paskah Lin Shou Fa Ong |     opaskah     |
|   23743373   |       Yuxin Gu         |    SoleilGU     |

## How to Launch Application
1. Create virtual environment
    1. For Windows/Mac
        >   python3 -m venv venv
2. Activate virtual environment
    1. For Windows
        >   .\venv\Scripts\activate
    2. For MacOS/Linux
        >   .venv/bin/activate
3. Install requirements
    >   pip install -r requirements.txt
4. Initiate database
    > flask db init
5. upgrade database
    > flask db upgrade
6. Run the application 
    >   flask --app application run --debug
7. Open the login register url
    1. Go to your browser and type http://localhost:5000/login-register/

## How to Run the Tests for the Application
1. assuming that coverage has been installed in the virtual environment
2. coverage run -m unittest tests/test_suite.py
3. coverage report to show the code coverage report
4. coverage html for more detail

## Page list
### Phase 1
- Login Register Page -> a page that tells the user to login, register or continue as guest
- All Puzzle Page ->  a page that shows all of the available puzzle in the database
- Create Wordle Puzzle Page -> a page where user can submit their own wordle puzzle for other people to solve
- Play Wordle Puzzle Page -> a page where user can play a wordle puzzle from the database

### Phase 2
- Profile Page -> a page that shows a list of puzzle that a certain user has created, a list of puzzle that user has solved and the user total score
- Leadboard Page -> a page that shows a list of top 5 score earner

## Feature List
### Phase 1
- create account
- log in account
- search wordle puzzle by wordle name or user who created the wordle 
- create wordle puzzle
- play wordle puzzle

### Phase 2
- see user profile
- see leaderboard score

## Possible additional feature?
- valid word checker when creating puzzle
- valid word checker when submitting guess
- give hint to the user
- automatically give difficulty tag to the puzzle based on number of letter and number of guess

References for asset
1. login_bar & signup_bar : https://m.twitch.tv/nojamjess/about
2. grey cat : https://www.pngsucai.com/png/2106631.html
3. daisy flower in 404 page: from Takaki Murakami （https://www.instagram.com/p/CY8f2S7L0iG/?igsh=MWFkYWxlNXo2Z2w4OA==）
4. play board & title frame : https://streamdps.com/panels/115695/
5. trophy: https://www.redbubble.com/i/sticker/Pixel-Gold-Trophy-Vector-Design-by-ercdesign/96400926.EJUG5
6. clouds : https://www.shutterstock.com/zh/image-vector/fluffy-clouds-pixel-art-icon-set-2135707491

## Tutorial or Reference Used
1. https://flask.palletsprojects.com/en/3.0.x/tutorial/layout/
