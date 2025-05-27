from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BlogPost(db.Model):
    __tablename__ = 'workout_app_blogpost'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
