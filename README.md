# Trivia API Game

This project is the final project in the Fullstack Developer nanodegree API course.

This project uses the Flask framework to implement a Trivia Game together with a Postgres database.

Backend code follows [PEP8 style guidelines](https://www.python.org/dev/peps/pep-0008/). 

Frontend are using react and this was already provided by Udacity from the start of the project.

## Getting Started

### Pre-requisites and Local Development 
Developers using this project should already have Python3, pip and node installed on their local machines. (use node16 for smooth integration)

#### Backend

##### Step 1: Set up and Populate the Database

1. With Postgres running, create a `trivia` database:

```
createdb trivia
```

2. From the `backend` folder in terminal, Populate the database using the `trivia.psql` file provided run:

```
psql trivia < trivia.psql
```

**Step 2: Install dependencies and start the server**

It is recommended to use a virutal enviroment (venv) to comply with the pythonic standards.

From the backend folder run `pip install requirements.txt`. All required packages are included in the requirements file. 

To run the application run the following commands (db username and password is enviroment variables for security reasons): 
```
export DATABASE_USERNAME="YOUR_USERNAME"
export DATABASE_PASSWORD="YOUR_PASSWORD"
export FLASK_APP=flaskr
export FLASK_ENV=development

flask run
```

These commands put the application in development and directs our application to use the `__init__.py` file in our flaskr folder. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made. Development has been done using WSL2.

The application is run on `http://127.0.0.1:5000/` by default and is a proxy in the frontend configuration. 

#### Frontend

From the frontend folder, run the following commands to start the client: 
```
nvm use 16  // Optional but frontend dont work with node version newer than 16
npm install // only once to install dependencies
npm start 
```

By default, the frontend will run on localhost:3000. 

### Tests
To deploy the tests, run the following to setup a test db:

```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
```

To deploy the tests, run:

```
python3 test_flaskr.py
```

All tests should pass if everything is setup correctly.

## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 404: Resource Not Found
- 422: Not Processable 

### Endpoints 
#### GET /questions
- General:
    - Returns a list of question objects, success value, list of categories and total number of questions
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`

``` {
{
  "categories": {
    "1": "Science",       
    "2": "Art", 
    "3": "Geography",     
    "4": "History",       
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "currentCategory": 1,   
  "questions": [
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Agra",
      "category": 3,
      "difficulty": 2,
      "id": 15,
      "question": "The Taj Mahal is located in which Indian city?"
    }
  ],
  "success": true,
  "totalQuestions": 22
}
```

#### GET /categories

- General:
  - Returns a list of category objects and a success value.
- Sample: `curl http://127.0.0.1:5000/categories`

``` {
{
  "categories": {
    "1": "Science",       
    "2": "Art",
    "3": "Geography",     
    "4": "History",       
    "5": "Entertainment", 
    "6": "Sports"
  },
  "success": true
}
```

#### DELETE /questions/{question_id}

- General:
  - Deletes the question of the given ID if it exists. Returns the id of the deleted question and a success value.
- `curl -X DELETE http://127.0.0.1:5000/questions/15`

```
{
  "deleted": 15,
  "success": true
}
```

#### POST /questions

- General:
    - Creates a new question using the submitted question, answer, category and difficulty. Returns the question, success value, answer, difficulty and category.
    - If any of the 4 submissions are None an error 422 will be returned.
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"What is 3+3?", "answer":"6", "category":"1", "difficulty":"2"}'`
```
{
  "answer": "6",
  "category": 1,
  "difficulty": 2,
  "question": "What is 3+3?",
  "success": true
}
```
#### POST /questions/search

- General:
  - Search for a question from a search term. Returns a list of question objects, success value (will be true even though no question match the search term), total questions and currect category.
  - Searching is not case sensitive and is using standard SQL LIKE for searching.
- `curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm":"+"}'`

```
{
  "currentCategory": 1,
  "questions": [
    {
      "answer": "4",
      "category": 1,
      "difficulty": 1,
      "id": 24,
      "question": "What is 2+2?"
    },
    {
      "answer": "44",
      "category": 1,
      "difficulty": 1,
      "id": 27,
      "question": "What is 2+42?"
    },
    {
      "answer": "8",
      "category": 1,
      "difficulty": 1,
      "id": 28,
      "question": "What is 2+6?"
    },
    {
      "answer": "6",
      "category": 1,
      "difficulty": 2,
      "id": 29,
      "question": "What is 3+3?"
    }
  ],
  "success": true,
  "totalQuestions": 22
}
```

#### GET /categories/{category_id}/questions

- General:
  - Can be used to see all questions in a category. Return a list of question objects, a success value, total amount of questions and current category
- Sample: `curl http://127.0.0.1:5000/categories/2/questions`

``` {
{
  "currentCategory": 2,
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "success": true,
  "totalQuestions": 22
}
```

#### POST /quizzes

- General:
  - Post endpoint to get questions to play a quiz. Takes category and previous questions and return a random question within the given category if provided (can play with all categories). A success value will also be returned.
  - 
- `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [24, 20],"quiz_category": {"type": "Science", "id": "1"}}'`

```
{
  "question": {
    "answer": "Blood",
    "category": 1,
    "difficulty": 4,
    "id": 22,
    "question": "Hematology is a branch of medicine involving the study of what?"
  },
  "success": true
}
```

Calling 1 more time will generate a new answer:

`curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [24, 20,22],"quiz_category": {"type": "Science", "id": "1"}}'`

```
{
  "question": {
    "answer": "44",
    "category": 1,
    "difficulty": 1,
    "id": 27,
    "question": "What is 2+42?"
  },
  "success": true
}
```


## Deployment N/A

## Authors
Mads Cornelius Andersen

## Acknowledgements 
Udacity for creating a good full stack developer course :).