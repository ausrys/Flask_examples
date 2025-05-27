import os


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:lopinis123@localhost:5432/workout"  # default
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
