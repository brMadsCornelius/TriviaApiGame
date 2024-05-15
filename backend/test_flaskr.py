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
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres:abc@{}/{}".format('localhost:5432', self.database_name)
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client

    
    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(data['categories'])

    def test_get_categories_fails(self):
        response = self.client().get('/categories/1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])

    def test_get_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(len(data["questions"]))
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(len(data["categories"]))

    def test_get_questions_fails(self):
        response = self.client().get('/questions?page=1000')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])

    def test_add_question(self):
        response = self.client().post('/questions', json={
            "question": "What is the capital of Egypt?",
            "answer": "Cairo",
            "category": "3",
            "difficulty": 2
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'], True)

    def test_add_question_fails(self):
        response = self.client().post('/questions', json={
            "question": "What is the capital of Egypt?",
            "answer": "Cairo",
            "category": "3"
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])

    def test_search_questions_with_result(self):
        response = self.client().post('/questions/search', json={"searchTerm": "?"}) # shold exist some questions with a question mark :-)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(data["questions"])

    def test_search_questions_without_result(self):
        response = self.client().post('/questions/search', json={"searchTerm": "I like big butts and i can not lie"}) # should not be a question :-)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data["questions"]), 0) # should return 0 questions

    def test_get_questions_from_category(self):
        category_id = 1  # just this category for testing
        response = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['questions'])
        self.assertEqual(data['currentCategory'], category_id)
        self.assertTrue(data['totalQuestions'])

    def test_get_questions_from_category_fails(self):
        category_id = 9999  # category 9999 does not exist
        response = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)

    def test_play_quiz(self):
        response = self.client().post('/quizzes', json={
            "previous_questions": [],
            "quiz_category": {"type": "Science", "id": 1}
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(data['question'])





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()