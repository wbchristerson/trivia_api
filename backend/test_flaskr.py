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
            self.valid_delete_id = q.id


    def tearDown(self):
        """Executed after reach test"""
        question_match_A = Question.query.filter(Question.question == "When is the best time to wear a striped sweater?").first()
        if question_match_A:
            question_match_A.delete()
        question_match_B = Question.query.filter(Question.question == "What color is grass?").first()
        if question_match_B:
            question_match_B.delete()

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
        self.assertEqual(19, data["total_questions"])
        self.assertEqual(len(expected_category_map), len(data["categories"]))
        for id, category in expected_category_map.items():
            self.assertIn(id, data["categories"])
            self.assertEqual(category, data["categories"][id])


    def test_get_questions_page_failure(self):
        """Test for retrieving page of questions with failure"""
        res = self.client().get('/questions?page=0')
        self.assertEqual(res.status_code, 422)


    def test_delete_question_success(self):
        """Test for deleting existent question by ID"""
        resBeforeDelete = self.client().get('/questions')
        dataBeforeDelete = json.loads(resBeforeDelete.data)

        total_question_count = dataBeforeDelete["total_questions"]

        resDelete = self.client().delete(f"/questions/{self.valid_delete_id}")
        dataDelete = json.loads(resDelete.data)

        self.assertEqual(resDelete.status_code, 200)
        self.assertTrue(dataDelete["success"])

        resAfterDelete = self.client().get('/questions')
        dataAfterDelete = json.loads(resAfterDelete.data)

        self.assertEqual(dataAfterDelete["total_questions"], total_question_count-1)


    def test_delete_question_failure(self):
        """Test for deleting non-existent question by ID"""
        res_delete = self.client().delete("/questions/1000000")
        self.assertEqual(res_delete.status_code, 404)


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


    def test_create_question_success(self):
        """Test for creating question successfully"""
        question_info = {
            "question": 'What color is grass?',
            "answer": 'Green',
            "category": 5,
            "difficulty": 2,
        }
        res = self.client().put('/questions', data=json.dumps(question_info), headers={'Content-Type': 'application/json'})
        self.assertEqual(200, res.status_code)
        data = json.loads(res.data)
        self.assertTrue("success" in data)
        self.assertTrue(data["success"])
        self.assertTrue("id" in data)

        question_match = Question.query.filter(Question.id == data["id"]).first()
        self.assertTrue(question_match is not None)
        self.assertEqual("What color is grass?", question_match.question)
        self.assertEqual("Green", question_match.answer)
        self.assertEqual(5, question_match.category)
        self.assertEqual(2, question_match.difficulty)


    def test_create_question_failure(self):
        """Test for failiing to create a question due to invalid parameter dictionary"""
        question_info = {
            "question": 'What color is grass?'
        }
        res = self.client().put('/questions', data=json.dumps(question_info), headers={'Content-Type': 'application/json'})
        self.assertEqual(400, res.status_code)


    def test_retrieve_category_questions_success(self):
        """Test for successful retrieval of category questions"""
        res = self.client().get('/categories/4/questions')
        self.assertEqual(200, res.status_code)
        data = json.loads(res.data)

        self.assertTrue("questions" in data)
        self.assertTrue("totalQuestions" in data)
        self.assertTrue("currentCategory" in data)

        self.assertEqual(5, data["totalQuestions"])
        self.assertEqual("History", data["currentCategory"])

        questions_matches = data["questions"]
        added_question = list(filter(lambda q: q["question"] == "When is the best time to wear a striped sweater?", questions_matches))

        self.assertTrue(added_question is not None)
        self.assertEqual(1, len(added_question))
        self.assertEqual("When is the best time to wear a striped sweater?", added_question[0]["question"])
        self.assertEqual("All the time.", added_question[0]["answer"])
        self.assertEqual(4, added_question[0]["category"])
        self.assertEqual(5, added_question[0]["difficulty"])


    def test_retrieve_category_questions_failure(self):
        """Test for failing to retrieve category questions"""
        res = self.client().get('/categories/8/questions')
        self.assertEqual(404, res.status_code)


    def test_retrieve_question_search_success(self):
        """Test for successful search of term 'title'"""
        search_info = { "page": 1, "searchTerm": 'title' }
        res = self.client().post('/questions', data=json.dumps(search_info), headers={'Content-Type': 'application/json' })
        self.assertEqual(200, res.status_code)

        data = json.loads(res.data)
        self.assertTrue("totalQuestions" in data)
        self.assertTrue("questions" in data)

        self.assertEqual(2, data["totalQuestions"])
        self.assertEqual(2, len(data["questions"]))

        data["questions"].sort(key = lambda q: q["question"])

        self.assertEqual("What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?", data["questions"][0]["question"])
        self.assertEqual("Edward Scissorhands", data["questions"][0]["answer"])
        self.assertEqual(5, data["questions"][0]["category"])
        self.assertEqual(3, data["questions"][0]["difficulty"])

        self.assertEqual("Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?", data["questions"][1]["question"])
        self.assertEqual("Maya Angelou", data["questions"][1]["answer"])
        self.assertEqual(4, data["questions"][1]["category"])
        self.assertEqual(2, data["questions"][1]["difficulty"])


    def test_retrieve_question_search_failure(self):
        """Test for failed search due to invalid input data"""
        search_info = { "page": 1 }
        res = self.client().post('/questions', data=json.dumps(search_info), headers={'Content-Type': 'application/json'})
        self.assertEqual(404, res.status_code)


    def test_retrieve_quiz_question_success(self):
        """Test for successful retrieval of multiple quiz questions"""
        previous_questions = []

        test_category_questions = Question.query.filter(Question.category == 1).all()
        category_question_ids = [q.id for q in test_category_questions]

        quiz_category = { "id": "1", "type": "Science" }
        quiz_info = { "previous_questions": previous_questions, "quiz_category": quiz_category }
        for _ in range(len(category_question_ids)):
            res = self.client().post('/quizzes', data=json.dumps(quiz_info), headers={'Content-Type': 'application/json' })
            self.assertEqual(200, res.status_code)
            data = json.loads(res.data)
            self.assertEqual(data["question"]["category"], 1)
            self.assertFalse(data["question"]["id"] in quiz_info["previous_questions"])
            self.assertTrue(data["question"]["id"] in category_question_ids)
            quiz_info["previous_questions"].append(data["question"]["id"])

        res = self.client().post('/quizzes', data=json.dumps(quiz_info), headers={'Content-Type': 'application/json' })
        self.assertEqual(200, res.status_code)
        data = json.loads(res.data)
        self.assertTrue(data["question"] is None)

    # No failure test for retrieval of quiz questions seemed necessary; the above test seemed to encompass all cases


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()