# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.


## Trivia API Documentation

### Introduction
The Trivia API is a simple API that provides the necessary data to the UdacityTrivia app, a quiz game app meant to bring teams in Udacity together. The API provides the data for categories and questions and contains other functionality that allows the frontend to function properly.

### Getting Started
- **Base URL:** The Trivia API has not been deployed yet and hence no domain is available. The default address when the API is run locally is http://localhost:5000.
- No API Keys or authentication is needed to use the Trivia API.

### Errors 
As with any application, errors can always occur. Errors are handled by returning a JSON object as the response when an error occurs.
There are 5 error status codes defined for the Trivia API:

- 404: resource not found
- 405: method not allowed
- 422: unprocessable entity
- 400: bad request
- 500: internal server error

A sample JSON error response is added below.

```json
{
   "success": False,
   "error": 500,
   "message": "internal server error"
}
 
 ```
### API Endpoints

#### GET /categories
Get all the available question categories.
**Returns** a JSON object containing all the available categories.

A sample request is shown below.

```
curl http://localhost:5000/categories
```
The response object returned when the request is successful is as shown below.

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports",
    "7": "Random Facts"
  },
  "success": true,
  "totalLength": 7
}
 
 ```
#### GET /questions
Get all the available questions.  
**Parameters**: page (default=1)  
**Returns** a JSON object containing all the available questions and categories.  
The data returned is paginated, returning 10 questions per page.

A sample request is shown below.

```
curl http://localhost:5000/questions
```
```
curl http://localhost:5000/questions?page=2
```
The response object returned when the request is successful is as shown below.

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports",
    "7": "Random Facts"
  },
  "questions": [
    {
      "answer": "Apollo 13",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    },
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Edward Scissorhands",
      "category": 5,
      "difficulty": 3,
      "id": 6,
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    },
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Brazil",
      "category": 6,
      "difficulty": 3,
      "id": 10,
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 23
}
 
 ```
 
 #### DELETE /questions/<int:question_id>
Delete the a given question using the question ID.  
**Returns** a JSON object containing a success message and the deleted question ID.

A sample request is shown below.

```
curl -X DELETE http://localhost:5000/questions/5
```
The response object returned when the request is successful is as shown below.

```json
{
  "deleted_question_id": 5,
  "success": true
}
 
 ```
 400: Resource not found error is returned if an invalid question ID is given.

#### POST /questions
Add a new question to the existing list of questions.  
**Parameters**: Question(String), Answer(String), Category(String), Difficulty Score(Integer).   
**Returns** a JSON object containing a success message and the newly created question ID.

A sample request is shown below.

```
curl -X POST http://localhost:5000/questions -H "Content-Type: application/json" -d '{"question": "Was Rome built in a day?", "answer": "
NO", "category": "4", "difficulty": 1}'
```
The response object returned when the request is successful is as shown below.

```json
{
  "question_id": 34,
  "success": true
}
 
 ```
 
 #### POST /questions/search
Search for questions that match a given search term.  
**Parameters**: searchTerm(String).   
**Returns** a JSON object containing a success message and all questions matching the given search term.

A sample request is shown below.

```
curl -X POST http://localhost:5000/questions/search -H "Content-Type: application/json" -d '{"searchTerm": "royal"}'
```
The response object returned when the request is successful is as shown below.

```json
{
  "questions": [
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "total_questions": 1
}
 
 ```
404: Resource(search term) not found error if no questions match the search term.

#### GET /categories/<int:category>/questions
Get all the available questions basesd on a selected category.
**Returns** a JSON object containing all the available questions per the selected category, the current category and all available categories.  
The data paginated with maximum of 10 quesions per page.

A sample request is shown below.

```
curl http://localhost:5000/categories/4/questions
```
The response object returned when the request is successful is as shown below.

```json
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports",
    "7": "Random Facts"
  },
  "current_category": "History",
  "questions": [
    {
      "answer": "Muhammad Ali",
      "category": 4,
      "difficulty": 1,
      "id": 9,
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Scarab",
      "category": 4,
      "difficulty": 4,
      "id": 23,
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    },
    {
      "answer": "NO",
      "category": 4,
      "difficulty": 1,
      "id": 26,
      "question": "Was Rome built in a day?"
    },
    {
      "answer": "NO",
      "category": 4,
      "difficulty": 1,
      "id": 29,
      "question": "Was Rome built in a day?"
    },
    {
      "answer": "NO",
      "category": 4,
      "difficulty": 1,
      "id": 30,
      "question": "Was Rome built in a day?"
    },
    {
      "answer": "NO",
      "category": 4,
      "difficulty": 1,
      "id": 31,
      "question": "Was Rome built in a day?"
    },
    {
      "answer": "NO",
      "category": 4,
      "difficulty": 1,
      "id": 32,
      "question": "Was Rome built in a day?"
    },
    {
      "answer": "NO",
      "category": 4,
      "difficulty": 1,
      "id": 33,
      "question": "Was Rome built in a day?"
    },
    {
      "answer": "NO",
      "category": 4,
      "difficulty": 1,
      "id": 34,
      "question": "Was Rome built in a day?"
    }
  ],
  "success": true,
  "total_questions": 10
}
 ```
#### POST /quizzes
Get next question if available in the selected category to play the trivia game.  
**Parameters**: previous_questions(Array), quiz_category(JSON Object (id(category_id) and type)), id(String), type(String).   
**Returns** a JSON object containing a success message and a question that matches the given category.

A sample request is shown below.

```
curl -X POST http://localhost:5000/quizzes -H "Content-Type: application/json" -d '{
                "previous_questions": [],
                "quiz_category": {
                    "id": "4",
                    "type": "History"}}'
```
The response object returned when the request is successful is as shown below.

```json
{
  "question": {
    "answer": "NO",
    "category": 4,
    "difficulty": 1,
    "id": 33,
    "question": "Was Rome built in a day?"
  },
  "success": true
}
 
 ```

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
