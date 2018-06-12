import datetime

from werkzeug.security import generate_password_hash
from flask_login import UserMixin

from myapp import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __init__(self, user_name, password):
        self.user_name = user_name
        self.password_hash = generate_password_hash(password)

    def __repr__(self):
        return '<User %r>' % self.username


class Post(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    post_time = db.Column(db.DateTime(), default=datetime.datetime.now())
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __repr__(self):
        return '<Post %r>' % self.title
