import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}:{}@{}/{}".format(os.environ.get('MY_PG_USER'), os.environ.get('MY_PG_PWD'), 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            q = Question("When is the best time to wear a striped sweater?", "All the time.", 4, 5)
            self.db.session.add(q)
            self.db.session.commit()

    
    def tearDown(self):
        """Executed after reach test"""
        question_match = Question.query.filter(Question.question == "When is the best time to wear a striped sweater?").first()
        if question_match:
            question_match.delete()

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories_success(self):
        """Test for retrieving all categories"""
        res = self.client().get('/')

        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        expected_categories = ['Science', 'Art', 'Geography', 'History', 'Entertainment', 'Sports']

        self.assertIn("categories", data)
        self.assertEqual(len(data["categories"]), len(expected_categories))
        for category in expected_categories:
            self.assertIn(category, data["categories"])

        self.assertIn("message", data)
        self.assertEqual(data["message"], "HELLO WORLD")


    def test_get_questions_page_success(self):
        """Test for retrieving a page of questions"""
        res = self.client().get('/questions?page=1')

        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)

        self.assertIn("questions", data)
        self.assertIn("total_questions", data)
        self.assertIn("categories", data)

        expected_category_map = {
            '1': "Science", '2': "Art", '3': "Geography", '4': "History", '5': "Entertainment",
            '6': "Sports"
        }

        self.assertEqual(10, len(data["questions"]))
        self.assertEqual(20, data["total_questions"])
        self.assertEqual(len(expected_category_map), len(data["categories"]))
        for id, category in expected_category_map.items():
            self.assertIn(id, data["categories"])
            self.assertEqual(category, data["categories"][id])


    def test_get_questions_page_failure(self):
        """Test for retrieving page of questions with failure"""
        res = self.client().get('/questions?page=0')
        self.assertEqual(res.status_code, 404)


    def test_retrieve_category_map_success(self):
        """Test for retrieving map of categories"""
        res = self.client().get('/categories')

        self.assertEqual(res.status_code, 200)

        data = json.loads(res.data)
        self.assertIn("categories", data)

        self.assertEqual(len(data["categories"]), 6)

        expected_category_map = { '1': "Science", '2': "Art", '3': "Geography", '4': "History",
                                  '5': "Entertainment", '6': "Sports" }

        for id, category in expected_category_map.items():
            self.assertIn(id, data["categories"])
            self.assertEqual(category, data["categories"][id])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()