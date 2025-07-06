from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt 
import datetime as dt

# This is the SQLAlchemy object that we will use to define our models (tables)
#milestone-2 completed
db = SQLAlchemy()
bcrypt = Bcrypt() 

# ----------------------
# User Table
# ----------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(100))
    qualification = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    role = db.Column(db.String(10), default='user')  # either 'admin' or 'user'
    scores = db.relationship('Score', backref='user', lazy=True)

    def __repr__(self):
        return f"<User {self.email}>"
    
    def check_password (self, password):
        return bcrypt.check_password_hash(self.password, password)
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8') #utf-8 converts from binary to text

# ----------------------
# Subject Table
# ----------------------
class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    chapters = db.relationship('Chapter', backref='subject', lazy=True)

    def __repr__(self):
        return f"<Subject {self.name}>"
# ----------------------
# Chapter Table
# ----------------------
class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True)

    def __repr__(self):
        return f"<Chapter {self.name}>"
# ----------------------
# Quiz Table
# ----------------------
class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)  # Quiz start date and time
    duration_hours = db.Column(db.Integer, default=0)  # Hours part of duration
    duration_minutes = db.Column(db.Integer, default=30)  # Minutes part of duration
    scores = db.relationship('Score', backref='quiz', lazy=True)
    questions = db.relationship('Question', backref='quiz', lazy=True)

    @property
    def end_datetime(self):
        """Calculate the end datetime based on start time and duration"""
        if not self.start_datetime:
            return None
        return self.start_datetime + dt.timedelta(hours=self.duration_hours, minutes=self.duration_minutes)

    IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
    @property
    def is_active(self):
        """Check if quiz is currently active based on start time and duration"""
        now = dt.datetime.now(IST)
        end_time = self.end_datetime
        if not self.start_datetime or not end_time:
            return False
        # Make sure start_datetime is timezone-aware
        start_time = self.start_datetime.replace(tzinfo=IST) if self.start_datetime.tzinfo is None else self.start_datetime
        end_time = end_time.replace(tzinfo=IST) if end_time.tzinfo is None else end_time
        return start_time <= now <= end_time

    def __repr__(self):
        return f"<Quiz {self.title}>"
# ----------------------
# Question Table
# ----------------------
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255), nullable=False)
    option4 = db.Column(db.String(255), nullable=False)
    correct_option = db.Column(db.Integer, nullable=False)  # 1, 2, 3, or 4

    def __repr__(self):
        return f"<Question {self.id}>"
# ----------------------
# Score Table
# ----------------------
class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer)
    date_taken = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Score User:{self.user_id} Quiz:{self.quiz_id} Score:{self.score}>"