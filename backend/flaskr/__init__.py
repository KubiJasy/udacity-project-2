import os
import random
from flask import Flask, request, abort, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate(request, selection):
    page = request.args.get('page', 1, type=int)
    start_index = (page - 1) * QUESTIONS_PER_PAGE
    end_index = start_index + QUESTIONS_PER_PAGE

    paginated_selection = selection[start_index:end_index]

    return paginated_selection


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    cors = CORS(app, resources={r"/*": {'origins': '*'}})

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        categories = Category.format_list(categories)

        if len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': categories,
            'totalLength': len(categories)
        })

    """
    @TODO:
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
        questions = Question.query.order_by(Question.id).all()
        paginated_questions = Question.format_list(
            paginate(request, questions))

        categories = Category.query.all()
        categories = Category.format_list(categories)
        # check that data was returned from the database query
        if len(paginated_questions) == 0 or len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'total_questions': len(questions),
            'questions': paginated_questions,
            'categories': categories,
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            # check that the question id exists in the database
            if question is None:
                abort(404)

            question.delete()

            return jsonify({
                'success': True,
                'deleted_question_id': question_id
            })
        except BaseException:
            abort(422)

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        data = request.get_json()
        # check that a valid post request was made with the necessary payload
        if data is None:
            abort(400)

        try:
            new_question = Question(
                question=data['question'],
                answer=data['answer'],
                category=data['category'],
                difficulty=int(
                    data['difficulty']))

            new_question.insert()

            question = Question.query.with_entities(
                Question.id).filter_by(question=data['question']).order_by(Question.id.desc()).first()
            question_id = question[0]

            return jsonify({
                'success': True,
                'question_id': question_id
            })
        except BaseException:
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        data = request.get_json()
        # check that a valid post request was made with the necessary payload
        if data is None:
            abort(400)
        try:
            search_string = data['searchTerm'].lower()
            results = Question.query.filter(Question.question.ilike(
                f'%{search_string}%')).order_by(Question.id).all()
            # check that data was returned from the database query
            if len(results) == 0:
                abort(404)

            paginated_questions = Question.format_list(
                paginate(request, results))

            return jsonify({
                'success': True,
                'total_questions': len(results),
                'questions': paginated_questions
            })

        except Exception as e:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.route('/categories/<int:category>/questions')
    def get_questions_per_category(category):
        questions = Question.query.filter_by(category=category).all()
        questions = Question.format_list(questions)

        categories = Category.query.all()
        categories = Category.format_list(categories)

        current_category = Category.query.filter_by(id=category).first().type
        # check that data was returned from the database query
        if len(questions) == 0 or len(categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'total_questions': len(questions),
            'questions': questions,
            'categories': categories,
            'current_category': current_category
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        data = request.get_json()
        # check that a valid post request was made with the necessary payload
        if data is None:
            abort(400)

        try:
            current_category = data['quiz_category']['id']
            previous_questions = data['previous_questions']

            # if statement for when a category has been selected

            if current_category != 0:
                question_ids = [id[0] for id in Question.query.with_entities(
                    Question.id).filter_by(category=current_category).all()]
                unplayed_question_ids = [
                    id for id in question_ids if id not in previous_questions]
                #  check if all the questions have been answered
                if not unplayed_question_ids:
                    return jsonify({
                        'success': True,
                        'question': None
                    })
                # return next unplayed question
                else:
                    next_question_id = unplayed_question_ids[random.randrange(
                        0, len(unplayed_question_ids))]
                    next_question = Question.query.get(
                        next_question_id).format()

                    return jsonify({
                        'success': True,
                        'question': {
                            'id': next_question_id,
                            'question': next_question['question'],
                            'answer': next_question['answer'],
                            'difficulty': next_question['difficulty'],
                            'category': next_question['category']
                        }
                    })
            # else condition for when all categories has been selected
            else:
                question_ids = [
                    id[0] for id in Question.query.with_entities(
                        Question.id).all()]
                unplayed_question_ids = [
                    id for id in question_ids if id not in previous_questions]
                #  check if all the questions have been answered
                if not unplayed_question_ids:
                    return jsonify({
                        'success': True,
                        'question': None
                    })
                # return next unplayed question
                else:
                    next_question_id = unplayed_question_ids[random.randrange(
                        0, len(unplayed_question_ids))]
                    next_question = Question.query.get(
                        next_question_id).format()

                    return jsonify({
                        'success': True,
                        'question': {
                            'id': next_question_id,
                            'question': next_question['question'],
                            'answer': next_question['answer'],
                            'difficulty': next_question['difficulty'],
                            'category': next_question['category']
                        }
                    })
        except Exception as e:
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    # define error handlers for various errors
    @app.errorhandler(404)
    def resource_not_found(error):
        return (
            jsonify({
                "success": False,
                "error": 404,
                "message": "resource not found"
            }),
            404
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, 
                     "error": 422,
                     "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(({"success": False,
                        "error": 400,
                       "message": "bad request"
                       }), 
                       400
                    )

    @app.errorhandler(405)
    def method_not_allowed(error):
        return (jsonify({"success": False, 
                         "error": 405,
                         "message": "method not allowed"}),
                          405, 
                )

    @app.errorhandler(500)
    def server_error(error):
        return (
            jsonify({
                "success": False,
                "error": 500,
                "message": "internal server error"
            }), 500
        )

    return app
