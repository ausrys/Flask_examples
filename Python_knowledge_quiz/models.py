from db import db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    options = db.relationship(
        'AnswerOption', backref='question', cascade="all, delete-orphan")


class AnswerOption(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String, nullable=False)
    is_correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.id'), nullable=False)


class UserAnswer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey(
        'question.id'), nullable=False)
    selected_option_id = db.Column(
        db.Integer, db.ForeignKey('answer_option.id'), nullable=False)


class UserActionLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    action = db.Column(db.String(50))  # 'login', 'logout'
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class UserQuizLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    score = db.Column(db.Integer)
    total = db.Column(db.Integer)
    percent = db.Column(db.Float)
    passed = db.Column(db.Boolean)
    duration_sec = db.Column(db.Integer)
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
