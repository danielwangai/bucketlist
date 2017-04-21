from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20))
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __repr__(self):
        return '<User %r>' % self.username


class Bucketlist(db.Model):
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship('Item', backref='bucketlist', lazy='dynamic')

    def __repr__(self):
        return '<Bucketlist %r>' % self.name


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def __repr__(self):
        return '<Task %r>' % self.name
