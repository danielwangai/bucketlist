from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bucketlist.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, first_name, last_name, username, email):
        self.id = id(self)
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username

class Bucketlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    done = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, name, user):
        self.id = id(self)
        self.name = name
        self.done = False
        self.created_at = datetime.utcnow()
        self.modified_at = None
        self.user = user
    
    def __repr__(self):
        return '<Bucketlist %r>' % self.name