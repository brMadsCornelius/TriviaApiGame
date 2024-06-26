import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

# Helper function to paginate questions
def paginate_questions(request, selection):
    page = request.args.get("page" , 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)
    CORS(app)

    """
    @DONE: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    """
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.order_by(Category.id).all()

        if len(categories) == 0:
            abort(404)

        formatted_categories = {category.id: category.type for category in categories}
        
        return jsonify({
            'success': True,
            'categories': formatted_categories
        })


    """
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        
        if len(current_questions)==0:
            abort(404)
        
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = {category.id: category.type for category in categories}

        return jsonify({
            'success': True,
            'questions': current_questions,
            'totalQuestions': len(Question.query.all()),
            'categories': formatted_categories,
            'currentCategory': 1 # Which one should be current? I am returning a list of questions with differnt categories??
        })


    """
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=["DELETE"])
    def delete_questions(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted': question_id
            })
        except:
            abort(422)


    """
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    @app.route('/questions', methods=["POST"])
    def add_questions():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        # Ensuer that frontend send all required data
        if new_question==None or new_answer==None or new_category==None or new_difficulty==None:
            abort(422)

        try:
            question = Question(question=new_question,answer=new_answer,category=new_category,difficulty=new_difficulty)

            question.insert()

            return jsonify({
                'success': True,
                'question':  question.question,
                'answer':  question.answer,
                'difficulty': question.difficulty,
                'category': question.category
            })
        except:
            abort(422)



    """
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=["POST"])
    def search_questions():
        body = request.get_json()

        try:
            searchTerm = body.get('searchTerm', None)
            
            selection = Question.query.filter(Question.question.ilike('%{}%'.format(searchTerm))).all()
            current_questions = paginate_questions(request, selection) # paginate max 10 questions

            return jsonify({
                'success': True,
                'questions': current_questions,
                'totalQuestions': len(Question.query.all()),
                'currentCategory': 1 # which should i response - it can be multiple categories??
            })
        except:
            abort(422)

    """
    @DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions')
    def get_questions_from_category(category_id):
        try:
            # Get all questions
            selection = Question.query.filter_by(category=str(category_id)).all()
            current_questions = paginate_questions(request, selection) # paginate max 10 questions

            if not current_questions:
                abort(404)

            return jsonify({
                'success': True,
                'questions': current_questions,
                'totalQuestions': len(Question.query.all()),
                'currentCategory': category_id
            })
        except:
            abort(404)
            


        
    """
    @DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def get_quiz_question():
        body = request.get_json()

        previous_questions = body.get('previous_questions', [])
        quiz_category = body.get('quiz_category', None)

        try:
            if quiz_category['id'] == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(category=quiz_category['id']).all()

            if questions == []:
                abort(404)

            # Filter out previous questions
            filtered_questions = []
            for question in questions:
                if question.id not in previous_questions:
                    filtered_questions.append(question)

            if len(filtered_questions) > 0:
                question = random.choice(filtered_questions).format()
            else:
                question = None

            return jsonify({
                'success': True,
                'question': question
            })
        except:
            abort(404)



    """
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(500)
    def serverSideError(error):
        return (
            jsonify({"success": False, "error": 500, "message": "Internal Server Error"}),
            500,
        )

    return app

