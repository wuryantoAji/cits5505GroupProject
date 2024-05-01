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

## Application Architecture Summary


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
5. migrate database
    > flask db migrate -m "your migration message"
6. upgrade database
    > flask db upgrade
7. Run the application 
    >   flask --app application run --debug
8. Open the hello world url
    1. Go to your browser and type http://localhost:5000/hello
## How to Run the Tests for the Application


## Page list
- Introductory view -> describe context and application purpose and allowing user to create an account and login
- Find Requests view -> allow user to search and accept requests
- Create Requests view -> allow user to create request for other people to answer

## Feature List
- create account
- log in account
- search request
- accept request (Need discussion on how to do this)
- do request (Need discussion on how to do this)
- create request
- view my own request

## Possible additional feature?
- .....

## Tutorial or Reference Used
1. https://flask.palletsprojects.com/en/3.0.x/tutorial/layout/
