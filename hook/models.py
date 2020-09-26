#! usr/env/bin python
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

members = db.Table('members',
                   db.Column('user_id', db.Integer,
                             db.ForeignKey('users.id'), primary_key=True),
                   db.Column('channel_id', db.Integer,
                             db.ForeignKey('channels.id'), primary_key=True)
                   )

messages_relations = db.Table('messages_relations',
                              db.Column('message_id', db.Integer,
                                        db.ForeignKey('messages.id')),
                              db.Column('channel_id', db.Integer,
                                        db.ForeignKey('channels.id')),
                              )


class User(db.Model):
    """
    Users Class for creating the 'users' table in the database
    and for managing user's information
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(10), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.Text, nullable=False)
    terms = db.Column(db.Boolean, unique=False, default=False)

    def __repr__(self):
        """
        Returns the user's username when the __str__ function is called.
        """
        return f"Username :{self.username}"

    def save(self):
        """ saves user's data """
        db.session.add(self)
        db.session.commit()


class Channel(db.Model):
    """
    Channel Model for creating the 'channels' table and managing channel
    related objects
    """
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(20), nullable=False)
    member = db.relationship('User', secondary=members, lazy='subquery',
                             backref=db.backref('members', lazy=True))

    def save(self):
        """ saves a channel and its data """
        db.session.add(self)
        db.session.commit()


class Message(db.Model):
    """Message table in the database"""
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.String(10), nullable=False)
    message = db.Column(db.Text, nullable=False)
    channel = db.relationship('Channel', secondary=messages_relations,
                              lazy='subquery',
                              backref=db.backref('messages_relations',
                                                 lazy=True)
                              )

    def save(self):
        """ saves messages """
        db.session.add(self)
        db.session.commit()


class MessageCreator:
    """
    Message function for adding messages to the Channel Class or channels table
    """
    def __init__(self, name, message):
        """ configure message's arguments """
        self.name = name
        self.timestamp = datetime.datetime.now()
        self.message = message
