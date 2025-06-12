from app import app
from db import db
from models import Question, AnswerOption

with app.app_context():
    # Optional: clear existing questions
    AnswerOption.query.delete()
    Question.query.delete()
    db.session.commit()

    questions_data = [
        {
            "text": "What is the output of: print(type([]))?",
            "options": [
                ("<class 'list'>", True),
                ("<class 'tuple'>", False),
                ("<class 'dict'>", False),
                ("<class 'set'>", False),
            ]
        },
        {
            "text": "What is the result of: len('Hello World')?",
            "options": [
                ("11", True),
                ("10", False),
                ("12", False),
                ("None", False),
            ]
        },
        {
            "text": "Which of the following is used to define a function in Python?",
            "options": [
                ("def", True),
                ("function", False),
                ("define", False),
                ("fun", False),
            ]
        },
        {
            "text": "What is the output of: print(3 == 3.0)?",
            "options": [
                ("True", True),
                ("False", False),
                ("Error", False),
                ("None", False),
            ]
        },
        {
            "text": "Which of the following is *not* a valid data type in Python?",
            "options": [
                ("array", True),
                ("list", False),
                ("tuple", False),
                ("dict", False),
            ]
        },
        {
            "text": "How do you start a comment in Python?",
            "options": [
                ("#", True),
                ("//", False),
                ("<!--", False),
                ("/**", False),
            ]
        },
        {
            "text": "Which keyword is used for exception handling?",
            "options": [
                ("try", True),
                ("handle", False),
                ("error", False),
                ("catch", False),
            ]
        },
        {
            "text": "What does the 'range(5)' function return?",
            "options": [
                ("0 to 4", True),
                ("1 to 5", False),
                ("0 to 5", False),
                ("1 to 4", False),
            ]
        },
        {
            "text": "What is the output of: print(bool('False'))?",
            "options": [
                ("True", True),
                ("False", False),
                ("Error", False),
                ("None", False),
            ]
        },
        {
            "text": "Which data type is immutable?",
            "options": [
                ("tuple", True),
                ("list", False),
                ("set", False),
                ("dict", False),
            ]
        },
        {
            "text": "Which method is used to add an item to a list?",
            "options": [
                ("append()", True),
                ("add()", False),
                ("insert()", False),
                ("push()", False),
            ]
        },
        {
            "text": "What is the result of: 5 // 2?",
            "options": [
                ("2", True),
                ("2.5", False),
                ("3", False),
                ("1", False),
            ]
        },
        {
            "text": "Which of these is a correct dictionary declaration?",
            "options": [
                ("{'a': 1, 'b': 2}", True),
                ("['a', 'b']", False),
                ("('a', 'b')", False),
                ("{'a', 'b'}", False),
            ]
        },
        {
            "text": "What does the 'pass' keyword do?",
            "options": [
                ("Does nothing", True),
                ("Stops loop", False),
                ("Skips next line", False),
                ("Raises an error", False),
            ]
        },
        {
            "text": "Which statement is used to exit a loop prematurely?",
            "options": [
                ("break", True),
                ("stop", False),
                ("exit", False),
                ("continue", False),
            ]
        },
        {
            "text": "What will be the output of: print(2**3)?",
            "options": [
                ("8", True),
                ("6", False),
                ("9", False),
                ("23", False),
            ]
        },
        {
            "text": "What is the default return value of a function that doesn't explicitly return anything?",
            "options": [
                ("None", True),
                ("0", False),
                ("False", False),
                ("undefined", False),
            ]
        },
        {
            "text": "Which of the following opens a file for reading in text mode?",
            "options": [
                ("open('file.txt', 'r')", True),
                ("open('file.txt', 'w')", False),
                ("open('file.txt', 'a')", False),
                ("open('file.txt', 'rb')", False),
            ]
        },
        {
            "text": "Which function returns the number of items in a list?",
            "options": [
                ("len()", True),
                ("count()", False),
                ("size()", False),
                ("length()", False),
            ]
        },
        {
            "text": "What will be the result of: type({})?",
            "options": [
                ("<class 'dict'>", True),
                ("<class 'set'>", False),
                ("<class 'list'>", False),
                ("<class 'tuple'>", False),
            ]
        },
        {
            "text": "Which of these is used to install external packages?",
            "options": [
                ("pip", True),
                ("npm", False),
                ("composer", False),
                ("yarn", False),
            ]
        },
        {
            "text": "What will be the output of: print('5' + '3')?",
            "options": [
                ("53", True),
                ("8", False),
                ("Error", False),
                ("15", False),
            ]
        },
        {
            "text": "Which one is *not* a valid Python keyword?",
            "options": [
                ("foreach", True),
                ("for", False),
                ("if", False),
                ("with", False),
            ]
        },
        {
            "text": "Which of the following is used to define an anonymous function?",
            "options": [
                ("lambda", True),
                ("anonymous", False),
                ("def", False),
                ("func", False),
            ]
        },
        {
            "text": "How do you convert a string '123' to an integer?",
            "options": [
                ("int('123')", True),
                ("str(123)", False),
                ("float('123')", False),
                ("int(123.0)", False),
            ]
        },
        {
            "text": "What does the 'is' operator check?",
            "options": [
                ("Object identity", True),
                ("Value equality", False),
                ("Data type", False),
                ("Syntax validity", False),
            ]
        },
        {
            "text": "Which exception is raised when dividing by zero?",
            "options": [
                ("ZeroDivisionError", True),
                ("ValueError", False),
                ("ArithmeticError", False),
                ("NameError", False),
            ]
        },
        {
            "text": "Which of these methods removes an item from a dictionary by key?",
            "options": [
                ("pop()", True),
                ("remove()", False),
                ("del()", False),
                ("discard()", False),
            ]
        },
        {
            "text": "Which of the following types is unordered?",
            "options": [
                ("set", True),
                ("list", False),
                ("tuple", False),
                ("dict", False),
            ]
        },
        {
            "text": "Which built-in function can be used to iterate over two lists simultaneously?",
            "options": [
                ("zip()", True),
                ("map()", False),
                ("filter()", False),
                ("enumerate()", False),
            ]
        },
        {
            "text": "What will the expression `not False` evaluate to?",
            "options": [
                ("True", True),
                ("False", False),
                ("None", False),
                ("Error", False),
            ]
        },
        {
            "text": "Which method is used to convert all characters in a string to lowercase?",
            "options": [
                ("lower()", True),
                ("downcase()", False),
                ("tolower()", False),
                ("casefold()", False),
            ]
        },
        {
            "text": "Which of the following statements creates a set?",
            "options": [
                ("set([1, 2, 3])", True),
                ("{1: 2, 3: 4}", False),
                ("[1, 2, 3]", False),
                ("(1, 2, 3)", False),
            ]
        },
        {
            "text": "What is the result of: print(None == False)?",
            "options": [
                ("False", True),
                ("True", False),
                ("None", False),
                ("Error", False),
            ]
        },
        {
            "text": "What does the 'continue' statement do?",
            "options": [
                ("Skips to next iteration", True),
                ("Stops loop", False),
                ("Exits program", False),
                ("Restarts loop", False),
            ]
        },
        {
            "text": "Which function is used to get user input in Python 3?",
            "options": [
                ("input()", True),
                ("raw_input()", False),
                ("scanf()", False),
                ("gets()", False),
            ]
        },
        {
            "text": "How is string formatting done in Python using f-strings?",
            "options": [
                ("f\"Hello {name}\"", True),
                ("format(\"Hello {name}\")", False),
                ("%s % name", False),
                ("string.format(name)", False),
            ]
        },
        {
            "text": "Which keyword is used to handle exceptions?",
            "options": [
                ("except", True),
                ("catch", False),
                ("throw", False),
                ("handle", False),
            ]
        },
        {
            "text": "Which module is commonly used for regular expressions?",
            "options": [
                ("re", True),
                ("regex", False),
                ("regexp", False),
                ("pattern", False),
            ]
        },
        {
            "text": "What is the output of: print(bool([]))?",
            "options": [
                ("False", True),
                ("True", False),
                ("Error", False),
                ("None", False),
            ]
        }
    ]

    for q in questions_data[:10]:
        question = Question(text=q["text"])
        db.session.add(question)
        db.session.flush()  # Get ID before adding options
        for option_text, is_correct in q["options"]:
            option = AnswerOption(
                text=option_text,
                is_correct=is_correct,
                question_id=question.id
            )
            db.session.add(option)

    db.session.commit()
    print("Seeded 40 questions into the database.")
