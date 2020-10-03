# Full Stack Trivia

This is a webpage to manage a trivia app and play the game. The front-end is minimal; the focus is on the back-end API used for accessing a postgresql database.

The application:

1) Displays questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer. 
2) Deletes questions.
3) Adds questions and require that they include question and answer text.
4) Searches for questions based on a text query string.
5) Plays the quiz game, randomizing either all questions or within a specific category. 

For more information about the frontend and backend (again the focus is on the backend):

1. [`./frontend/`](./frontend/README.md)
2. [`./backend/`](./backend/README.md)

## About the Stack

The key functional areas are:

### Backend

The `./backend` directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in app.py to define your endpoints and can reference models.py for DB and SQLAlchemy setup. 

### Frontend

The `./frontend` directory contains a complete React frontend to consume the data from the Flask server. You will need to update the endpoints after you define them in the backend. Those areas are marked with TODO and can be searched for expediency. 

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. 

[View the README.md within ./frontend for more details.](./frontend/README.md)
