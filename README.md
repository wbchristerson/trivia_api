# Full Stack Trivia

Hold trivia games on a regular basis and create a  webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out. 

Finish the trivia app so trivia games can be held and see who's the most knowledgeable of the bunch. The application:

1) Displays questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Deletes questions.
3) Adds questions and require that they include question and answer text.
4) Searches for questions based on a text query string.
5) Plays the quiz game, randomizing either all questions or within a specific category. 

## Tasks

There are `TODO` comments throughout project. Start by reading the READMEs in:

1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)

We recommend following the instructions in those files in order. This order will look familiar from our prior work in the course.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the [project repository]() and [Clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom. 

## About the Stack

We started the full stack application for you. It is desiged with some key functional areas:

### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in app.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup. 

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. You will need to update the endpoints after you define them in the backend. Those areas are marked with TODO and can be searched for expediency. 

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. 

[View the README.md within ./frontend for more details.](./frontend/README.md)
