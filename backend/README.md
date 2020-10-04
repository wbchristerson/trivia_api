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

### Endpoints

REVIEW_COMMENT
```
This README is missing documentation of your endpoints. Below is an example for your endpoint to get all categories. Please use it as a reference for creating your documentation and resubmit your code. 

Endpoints
GET '/categories'
GET ...
POST ...
DELETE ...

GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}

```


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```