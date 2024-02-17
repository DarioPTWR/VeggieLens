from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    """
    User model for storing user details.

    Attributes:
        id (int): Unique identifier for the user, serves as the primary key.
        email (str): The user's email address, must be unique.
        username (str): The user's chosen username, must be unique.
        password (str): The user's password.
    """
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True) # Primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(1000), unique=True)
    password = db.Column(db.String(100))

class Entry(db.Model):
    """
    Entry model for storing information about each prediction entry.

    Attributes:
        id (int): Unique identifier for the entry, auto-incremented and serves as the primary key.
        user (int): Identifier for the user who made the prediction. Foreign key to User.id.
        filePath (str): Path to the file used for prediction.
        modelType (str): Type of model used for making the prediction.
        imageSize (str): Size of the image used in the prediction.
        prediction (int): The numerical prediction result.
        predicted_on (DateTime): The date and time when the prediction was made.
    """
    __tablename__ = 'Entry'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer)
    filePath = db.Column(db.String)
    modelType = db.Column(db.String)
    imageSize = db.Column(db.String)
    prediction = db.Column(db.Integer)
    predicted_on = db.Column(db.DateTime, nullable=False)

class Quiz(db.Model):
    """
    Quiz model for storing quiz attempts and scores.

    Attributes:
        id (int): Unique identifier for the quiz attempt, auto-incremented and serves as the primary key.
        user (int): Identifier for the user who took the quiz. Foreign key to User.id.
        modelType (str): Type of model used for the quiz.
        imageSize (str): Size of the images used in the quiz.
        imgs (str): A string representation of the images used in the quiz.
        userScore (Numeric): The score obtained by the user.
        veggieLensScore (Numeric): The score obtained by the system or the 'correct' score.
        quiz_on (DateTime): The date and time when the quiz was taken.
    """
    __tablename__ = 'QuizEntry'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user = db.Column(db.Integer)
    modelType = db.Column(db.String)
    imageSize = db.Column(db.String)
    imgs = db.Column(db.String)
    userScore = db.Column(db.Numeric(precision=10, scale=2))
    aiScore = db.Column(db.Numeric(precision=10, scale=2))
    quiz_on = db.Column(db.DateTime, nullable=False)