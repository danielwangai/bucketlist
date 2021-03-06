"""To define db models and their properties."""
import os
from datetime import datetime

from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

from app import db


class User(db.Model):
    """To define user properties."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password = db.Column(db.String(128))
    bucketlists = db.relationship('Bucketlist', backref='user',
                                  cascade='all,delete', lazy='dynamic')

    def generate_auth_token(self, expiration=40000):
        """To generate auth token."""
        s = Serializer(os.environ['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        """To verify token."""
        s = Serializer(os.environ['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    def __repr__(self):
        return '<User %r>' % self.username


class Bucketlist(db.Model):
    """To define bucketlist properties."""

    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship('Item', backref='bucketlist',
                            cascade='all, delete', lazy='dynamic')

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": str(self.created_at),
            "modified_at": str(self.modified_at),
            "created_by": self.created_by,
            "items": [{item.to_json} for item in self.items]
        }

    def __repr__(self):
        return '<Bucketlist %r>' % self.name


class Item(db.Model):
    """To define item properties."""

    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.now)
    modified_at = db.Column(db.DateTime, default=datetime.now)
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at,
            "modified_at": self.modified_at,
            "done": self.done,
            "bucketlist_id": self.bucketlist_id
        }

    def __repr__(self):
        return '<Item %r>' % self.name
