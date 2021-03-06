import os
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import sys
from models import setup_db, Question, Category
from random import randint


QUESTIONS_PER_PAGE = 10


def get_page_range(all_records, page):
  '''Given a page number, return the records of all_records indexed at positions QUESTIONS_PER_PAGE * (page-1) up to
    QUESTIONS_PER_PAGE * page - 1 inclusive. If the page < 1, raise an error. If the described page range would go
    beyond the length of the array of all_records, return up to the end of the array (returning an empty array if
    the page range is completely beyond the length of the array).
  '''
  if page < 1:
    raise ValueError(f"Page {page} does not exist.")
  range_start = min((page - 1) * QUESTIONS_PER_PAGE, len(all_records))
  range_end = min(page * QUESTIONS_PER_PAGE, len(all_records))
  return [db_question.format() for db_question in all_records[range_start:range_end]]


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  app.secret_key = os.urandom(32)
  setup_db(app)

  '''
  This sets up CORS. It allows '*' for origins.
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  The after_request decorator is used to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Ty[e, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
    return response

  '''
  An endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/')
  def retrieve_all_categories():
    try:
      all_categories = Category.query.all()
      return jsonify({
        'message': 'HELLO WORLD',
        'categories': [category.type for category in all_categories]
      })
    except:
      # print(sys.exc_info())
      flash('An error occurred.')
      abort(500)


  @app.route('/categories')
  def retrieve_category_map():
    try:
      all_categories = Category.query.all()
      return jsonify({
        'categories': { category.id : category.type for category in all_categories }
      })
    except Exception as ex:
      # print(sys.exc_info())
      flash(f"An error occurred when attempting to fetch all categories: {ex}.")
      abort(422)


  '''
  An endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint returns a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions', methods=['GET'])
  def questions():
    page = int(request.args.get("page", "1"))

    try:
      all_questions = Question.query.all()
      range_questions = get_page_range(all_questions, page)
      all_categories = Category.query.all()
      return jsonify({
        'questions': range_questions,
        'total_questions': len(all_questions),
        'categories': { category.id: category.type for category in all_categories },

        # How can the "current category" be determined?
      })
    except Exception as ex:
      # print(sys.exc_info())
      flash(f"An error occurred when attempting to fetch page {page}: {ex}.")
      abort(422)

  '''
  An endpoint to DELETE a question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/questions/<question_id>', methods=['DELETE'])
  def delete_question(question_id):
    error_code = None
    try:
      question = Question.query.filter(Question.id == question_id).first()
      if question is None:
        raise ValueError(f"There is no problem with id {question_id}.")
      question.delete()
      flash(f"Question removed - id: {question_id}")
    except Exception as ex:
      error_code = 404
      # print(sys.exc_info())
      flash(f"An error occurred: {ex}")

    if error_code:
      abort(error_code)
    return jsonify({ "success": True })

  '''
  An endpoint to POST a new question, 
  which requires the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  # A put request seemed more appropriate to me here, also to avoid collision with the already-
  # named post request with this URL.
  @app.route('/questions', methods=['PUT'])
  def create_question():
    error_code = None
    question_id = None
    try:
      body = request.get_json()
      fields = ["question", "answer", "category", "difficulty"]

      for field in fields:
        if body.get(field) is None:
          raise ValueError(f"The request does not include a field for {field}.")

      if not isinstance(body.get("difficulty"), int):
        raise ValueError("The request does not include an integer-valued difficulty.")

      if not (1 <= body.get("difficulty") <= 5):
        raise ValueError("The request difficulty is not within the allowed range of 1 to 5 inclusive.")

      question = Question(body.get("question"), body.get("answer"), body.get("category"),
                          body.get("difficulty"))
      question.insert()
      question_id = question.id
      flash("Question successfully added.")
    except Exception as ex:
      error_code = 400
      # print(sys.exc_info())
      flash(f"An error occurred: {ex}")

    if error_code:
      abort(error_code)

    return jsonify({ "success": True, "id": question_id })


  '''
  A POST endpoint to get questions based on a search term. 
  It returns any questions for which the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/questions', methods = ['POST'])
  def retrieve_question_search():
    try:
      body = request.get_json()
      page = body.get("page", 1)

      if 'searchTerm' not in body:
        raise ValueError("Improperly formatted request")
      matching_questions = Question.query.filter(Question.question.like("%" + body["searchTerm"] + "%")).all()
      return jsonify({
        'totalQuestions': len(matching_questions),
        'questions': get_page_range(matching_questions, page),
      })
    except Exception as ex:
      flash(f"An error occurred when attempting to fetch questions matching the search: {ex}")
      abort(404)


  '''
  A GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<category_id>/questions')
  def retrieve_category_questions(category_id):
    try:
      page = int(request.args.get("page", "1"))
      # all_questions = Question.query.all()

      matching_category = Category.query.filter_by(id = category_id).first()

      if matching_category is None:
        raise ValueError("No matching category")

      matching_category_type = matching_category.type

      all_questions = Question.query.filter(Question.category == category_id).all()

      total_questions = len(all_questions)

      matching_questions = get_page_range(all_questions, page)
      return jsonify({
        'questions': matching_questions,
        'totalQuestions': total_questions,
        'currentCategory': matching_category_type,
      })
    except Exception as ex:
      flash(f"An error occurred when attempting to fetch the questions for the category with id {category_id}: {ex}")
      abort(404)


  '''
  A POST endpoint to get questions to play the quiz. 
  This endpoint takes a category parameter and a previous question parameter
  and returns a random question within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''
  @app.route('/quizzes', methods = ['POST'])
  def retrieve_quiz_question():
    try:
      body = request.get_json()
      matching_question_list = Question.query.filter(Question.category == int(body["quiz_category"]["id"])).filter(Question.id.notin_(body["previous_questions"])).all()

      if len(matching_question_list) == 0:
        return jsonify({
          'question': None
        })
      else:
        chosen_index = randint(0, len(matching_question_list)-1)
        return jsonify({
          'question': matching_question_list[chosen_index].format(),
        })
    except Exception as ex:
      flash(f"An error occurred when selecting a new question for the quiz: {ex}")
      # print(sys.exc_info())
      # print(str(ex))
      abort(404)


  '''
  Error handlers for all expected errors: 400, 404, 422, 500. 
  '''
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False,
      "error": 400,
      "message": f"The request was malformed: {error}"
    }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message": f"The resource was not found: {error}"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": f"The request was properly formatted but it could not be processed: {error}",
    }), 422

  @app.errorhandler(500)
  def internal_server_error(error):
    return jsonify({
      "success": False,
      "error": 500,
      "message": f"There was an internal server error: {error}"
    }), 500

  return app

    