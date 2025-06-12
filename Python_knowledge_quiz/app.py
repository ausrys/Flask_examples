from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, \
    session
from werkzeug.security import generate_password_hash, check_password_hash
import random
from db import db
from models import User, AnswerOption, Question, UserActionLog, UserAnswer, UserQuizLog

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Config SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
# Create tables
with app.app_context():
    db.create_all()


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session["user_id"] = user.id  # ✅ Store logged-in user ID
            log = UserActionLog(user_id=user.id, action="login")
            db.session.add(log)
            db.session.commit()
            return redirect(url_for("qualification"))  # Or dashboard
        else:
            error = "Invalid credentials. Please try again."

    return render_template("login.html", error=error)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        if User.query.filter_by(email=email).first():
            flash("Email already exists!")
            return render_template("register.html")

        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash("Registration successful. Please login.")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/qualification", methods=["GET", "POST"])
def qualification():

    if "user_id" not in session:
        return redirect(url_for("login"))
    user_id = session["user_id"]
    # # ✅ Check if user already completed the quiz
    if UserAnswer.query.filter_by(user_id=user_id).count() > 0:
        return redirect(url_for("results"))
    if request.method == "GET":
        session["quiz_start"] = datetime.utcnow().isoformat()
    if request.method == "POST":
        quiz_start = datetime.fromisoformat(session.get("quiz_start"))
        quiz_end = datetime.utcnow()
        duration = (quiz_end - quiz_start).total_seconds()

        score = 0
        total = 0
        user_id = session["user_id"]
        for key, value in request.form.items():
            if key.startswith("question_"):
                question_id = int(key.split("_")[1])
                selected_option_id = int(value)
                total += 1

                question = Question.query.get(question_id)
                correct = next(
                    (opt for opt in question.options if opt.is_correct), None)

                if selected_option_id == correct.id:
                    score += 1

                answer = UserAnswer(
                    user_id=user_id,
                    question_id=question_id,
                    selected_option_id=selected_option_id
                )
                db.session.add(answer)
        percent = (score / total) * 100
        passed = percent >= 80
        quiz_log = UserQuizLog(
            user_id=user_id,
            score=score,
            total=total,
            percent=percent,
            passed=passed,
            duration_sec=int(duration),
            submitted_at=quiz_end
        )
        db.session.add(quiz_log)
        db.session.commit()
        return redirect(url_for("results"))

    # GET: Fetch and shuffle questions and options
    questions = Question.query.all()
    random.shuffle(questions)

    for q in questions:
        q.options = sorted(q.options, key=lambda x: random.random())

    return render_template("qualification.html", questions=questions)


@app.route("/results")
def results():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]
    answers = UserAnswer.query.filter_by(user_id=user_id).all()

    results = []
    score = 0

    for ans in answers:
        question = Question.query.get(ans.question_id)
        selected = AnswerOption.query.get(ans.selected_option_id)
        correct = next(
            (opt for opt in question.options if opt.is_correct), None)

        is_correct = selected.id == correct.id
        if is_correct:
            score += 1

        results.append({
            "question": question.text,
            "selected": selected.text,
            "correct": correct.text,
            "is_correct": is_correct
        })

    percent = (score / len(answers)) * 100
    passed = percent >= 80

    return render_template("results.html", score=score, total=len(answers),
                           results=results, percent=percent, passed=passed)


@app.route("/logout")
def logout():
    if "user_id" in session:
        log = UserActionLog(user_id=session["user_id"], action="logout")
        db.session.add(log)
        db.session.commit()
    session.clear()  # Remove all session data
    return redirect(url_for("login"))


@app.route("/leaderboard")
def leaderboard():
    top_results = (
        UserQuizLog.query
        .join(User)
        .add_columns(User.email, UserQuizLog.score, UserQuizLog.total,
                     UserQuizLog.percent, UserQuizLog.duration_sec,
                     UserQuizLog.submitted_at)
        .order_by(UserQuizLog.percent.desc(), UserQuizLog.duration_sec.asc())
        .limit(10)
        .all()
    )
    return render_template("leaderboard.html", results=top_results)


@app.route("/admin/logs")
def admin_logs():
    user_logs = (
        UserActionLog.query
        .join(User)
        .add_columns(User.email, UserActionLog.action, UserActionLog.timestamp)
        .order_by(UserActionLog.timestamp.desc())
        .limit(10)
        .all()
    )

    quiz_logs = (
        UserQuizLog.query
        .join(User)
        .add_columns(User.email, UserQuizLog.score, UserQuizLog.total,
                     UserQuizLog.percent, UserQuizLog.duration_sec,
                     UserQuizLog.submitted_at, UserQuizLog.passed)
        .order_by(UserQuizLog.submitted_at.desc())
        .limit(10)
        .all()
    )

    return render_template("admin_logs.html", user_logs=user_logs, quiz_logs=quiz_logs)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
