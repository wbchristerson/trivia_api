import os
from flask import Flask, request, abort, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import sys

from models import setup_db, Question, Category

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
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Ty[e, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, PATCH, DELETE, OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
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
      abort(404)


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
      abort(404)


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
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
      })
    except Exception as ex:
      # print(sys.exc_info())
      flash(f"An error occurred when attempting to fetch page {page}: {ex}.")
      abort(404)

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

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
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
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

      question = Question(body.get("question"), body.get("answer"), body.get("category"),
                          body.get("difficulty"))
      question.insert()
      question_id = question.id
      flash("Question successfully added.")
    except Exception as ex:
      error_code = 404
      # print(sys.exc_info())
      flash(f"An error occurred: {ex}")

    if error_code:
      abort(error_code)

    return jsonify({ "success": True, "id": question_id })


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
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
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/categories/<category_id>/questions')
  def retrieve_category_questions(category_id):
    try:
      page = int(request.args.get("page", "1"))
      all_questions = Question.query.all()
      total_questions = len(all_questions)

      matching_category = Category.query.filter_by(id = category_id).first()

      if matching_category is None:
        raise ValueError("No matching category")

      matching_category_type = matching_category.type
      matching_questions = get_page_range(list(filter(lambda q: q.category == int(category_id), all_questions)), page)
      return jsonify({
        'questions': matching_questions,
        'totalQuestions': total_questions,
        'currentCategory': matching_category_type,
      })
    except Exception as ex:
      flash(f"An error occurred when attempting to fetch the questions for the category with id {category_id}: {ex}")
      abort(404)


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app

    