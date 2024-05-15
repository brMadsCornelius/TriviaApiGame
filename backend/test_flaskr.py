import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from settings import DATABASE_USERNAME, DATABASE_PASSWORD, DATABASE_TEST_NAME


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.database_path = f"postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost:5432/{DATABASE_TEST_NAME}"
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })
        self.client = self.app.test_client

        self.new_question = {
        "question": "What is the capital of Egypt?",
        "answer": "Cairo",
        "category": "3",
        "difficulty": 2
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            # Add a sample question to be used in tests
            sample_question = Question(
                question=self.new_question["question"],
                answer=self.new_question["answer"],
                category=self.new_question["category"],
                difficulty=self.new_question["difficulty"]
            )
            self.db.session.add(sample_question)
            self.db.session.commit()

            self.sample_question_id = sample_question.id  # Store the ID only


    
    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    """
    DONE
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

    
    def test_delete_question(self):
        with self.app.app_context():
            # Ensure the sample question exists by querying it within the context
            question_id = self.sample_question_id
            question = Question.query.get(question_id)
            self.assertIsNotNone(question)

            # Delete the question
            response = self.client().delete(f'/questions/{question_id}')
            data = json.loads(response.data)

            self.assertEqual(response.status_code, 200)
            self.assertTrue(data['success'])
            self.assertEqual(data['deleted'], question_id)

            # Verify the question has been deleted
            question = Question.query.filter(Question.id == question_id).one_or_none()
            self.assertIsNone(question)

    def test_delete_question_not_found(self):
        # Attempt to delete a question that does not exist
        response = self.client().delete('/questions/999abc9999')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data.get('success'))

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

    def test_play_quiz_invalid_category(self):
        response = self.client().post('/quizzes', json={
            "previous_questions": [],
            "quiz_category": {"type": "Unknown", "id": 9999}  # Invalid category ID
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)

    def test_404_error_handler(self):
        response = self.client().get('/nonexistent_route')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], 'resource not found')

    def test_422_error_handler(self):
        response = self.client().post('/questions', json={})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'])
        self.assertEqual(data['error'], 422)
        self.assertEqual(data['message'], 'unprocessable')



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()