# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Optional Virtual Enviornment

If you wish to work within a virtual environment to keep your dependencies for each project separate and organized, instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies

Whether or not you use a virtual environment, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM (object relational mapping) I used to handle the database. Most of the logic is set up in  `app.py` and references `models.py`. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension I used to handle cross origin requests from the frontend server. 

## Database Setup
With Postgres running, restore a database using the `trivia.psql` file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

If using a username, you may instead need to use the command:
```bash
psql -U <username> trivia < trivia.psql
```
and you may have to provide the password associated with `<username>` if there is any.

## Running the server

From within the `backend` directory, if you are using a virtual environment, first ensure you are working using that created virtual environment.

Execute the following lines to set up environment variables and start the server:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
export MY_PG_USER=<your postgres user>
export MY_PG_PWD=<your postgres password>
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application.

## API Reference

### General Notes

- Base URL: This project can only currently be run locally and is not hosted as a base URL. If the project is deployed in the future, the URL will change. The backend app is hosted at the default `http://127.0.0.1:5000/` (also known as `http://localhost:5000`), which is set as a proxy in the frontend configuraiton.
- Authentication: This version of the application does not require authentication or API keys.

### Error Handling

Errors are returned as JSON objects in the following format:
```json
{
  "success": false,
  "error": 400,
  "message": "The request was malformed."
}
```

The API returns four error types when requests fail:

- 400: Bad request
- 404: Resource not found
- 422: Not processable
- 500: Internal server error

### Endpoints

- GET '/'
- GET '/categories'
- GET '/questions'
- DELETE '/questions/<question_id>'
- PUT '/questions'
- POST '/questions'
- GET '/categories/<category_id>/questions'
- POST '/quizzes'

GET '/'

- Fetches a list of all category names
- Request arguments: None
- Returns: an object with a key "message" set to `'HELLO WORLD'` (simply as a status check) and another key "categories" which is the static list of categories
- Sample: `curl http://127.0.0.1:5000/`. Response:
```json
{
  "categories": [
    "Science", 
    "Art", 
    "Geography", 
    "History", 
    "Entertainment", 
    "Sports"
  ], 
  "message": "HELLO WORLD"
}
```

GET '/categories'
- Request arguments: None
- Returns: dictionary with keys of category IDs and values of category type strings
- Sample: `curl http://127.0.0.1:5000/categories`. Response:
```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }
}
```

GET '/questions'

- Request arguments: `"page"`, a positive integer used as the page of pagination for the request (questions are returned in page sizes of 10)
- Returns: dictionary containing a key `'questions'` with value a list of question objects, a key `'total_questions'` with value being the total number of questions, and a key `'categories'` with value of a dictionary of category IDs to category type strings.
- Sample: `curl http://127.0.0.1:5000/questions?page=1`. Response:
```json
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
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
  "total_questions": 19
}
```

DELETE '/questions/<question_id>'

- Request arguments: `question_id`, the ID of the question to be deleted
- Returns: dictionary with key `"success"` and value `true`.
- Sample: `curl -X "DELETE" http://127.0.0.1:5000/questions/5`. Response:
```json
{
  "success": true
}
```

PUT '/questions'

- Creates a new question record
- Request arguments: a dictionary containing keys:
    * "question": string
    * "answer": string
    * "category": positive integer (an id)
    * "difficulty": positive integer between 1 and 5 inclusive
- Returns: dictionary with entries:
    * "success": value of `True`
    * "id": the generated question's id
- Sample: `curl -H "Content-Type: application/json" -X "PUT" -d '{"question": "Steel is an alloy of carbon and what other element?", "answer": "Iron", "difficulty": 2, "category": 1}' http://127.0.0.1:5000/questions`. Response:
```json
{
  "id": 26, 
  "success": true
}
```

POST '/questions'

- Retrieves a paginated list of question objects matching a search query (with a page size of 10)
- Request arguments:
    * "searchTerm": string
    * "page" (optional): int (positive integer)
- Returns: dictionary with entries:
    * "totalQuestions": total number of questions matching search query
    * "questions": a paginated list of question objects with questions matching the search query
- Sample: `curl -H "Content-Type: application/json" -X "POST" -d '{"searchTerm": "title", "page": 1}' http://127.0.0.1:5000/questions`. Response:
```json
{
  "questions": [
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 25, 
      "question": "Whose autobiography is entitled \"I Know Why The Caged Bird Sings\"?"
    }
  ], 
  "totalQuestions": 2
}
```

GET '/categories/<category_id>/questions'

- Retrieves a paginated list of question objects matching a specific category ID (with a page size of 10)
- Request arguments:
    * `<category_id>` (in URL): ID of the category to filter by (in the sample database data provided, this includes 1 for "Science", 2, for "Art", 3 for "Geography", etc.)
    * "page" (optional): int (positive integer)
- Returns a dictionary with entries:
    * "questions": paginated list of matching questions
    * "totalQuestions": total number of questions in the database corresponding to the specified category ID
    * "currentCategory": the name of the category matching the specified category ID
- Sample: `curl -H "Content-Type: application/json" -X "GET" -d '{"page": 1}' http://127.0.0.1:5000/categories/1/questions`. Response:
```json
{
  "currentCategory": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": 1, 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": 1, 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": 1, 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Iron", 
      "category": 1, 
      "difficulty": 2, 
      "id": 26, 
      "question": "Steel is an alloy of carbon and what other element?"
    }
  ], 
  "totalQuestions": 4
}
```

POST '/quizzes'

- Retrieves a question from the specified category with an ID which is not among the list of already provided question IDs
- Request arguments:
    * "quiz_category": dictionary including a "type" and "id" key with values of the category name and ID, respectively
    * "previous_questions": list of IDs of questions previously added, which therefore should not be returned
- Returns a dictionary with a single key of "question" and a value of a randomly selected question object to return which does not correspond to one of the IDs in the request's previously asked questions
- Sample: `curl -H "Content-Type: application/json" -X "POST" -d '{"quiz_category": {"id": 1, "type": "Science"}, "previous_questions": [20, 22]}' http://127.0.0.1:5000/quizzes`. Response:
```json
{
  "question": {
    "answer": "Alexander Fleming", 
    "category": 1, 
    "difficulty": 3, 
    "id": 21, 
    "question": "Who discovered penicillin?"
  }
}
```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```