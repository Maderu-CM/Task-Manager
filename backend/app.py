from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv('.flaskenv')

app = Flask(__name__)

# Configuration of SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)
CORS(app)

migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, nullable=False, unique=True, autoincrement=True, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    projects = db.relationship('Project', backref='user', lazy=True)
    tasks = db.relationship('Task', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, nullable=False, unique=True, autoincrement=True, primary_key=True)
    title = db.Column(db.String(30), unique=True, nullable=False)
    objective = db.Column(db.String(200), nullable=False)
    category=db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    tasks = db.relationship('Task', backref='project', lazy=True)
    reviews = db.relationship('Review', backref='project', lazy=True)


class Task(db.Model):
    __tablename__ = 'task'

    id = db.Column(db.Integer, nullable=False, unique=True, autoincrement=True, primary_key=True)
    title = db.Column(db.String(30), unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    priority = db.Column(db.String(10), nullable=False)
    start_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    due_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(200), nullable=False)


class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, nullable=False, unique=True, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    comment = db.Column(db.String(200))


class Rating(db.Model):
    __tablename__ = 'rating'

    id = db.Column(db.Integer, nullable=False, unique=True, autoincrement=True, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    feedback = db.Column(db.String(200))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

import routes

if __name__ == '__main__':
    app.run(debug=True)
