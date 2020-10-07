#!usr/bin/env python
from flask_sqlalchemy import SQLAlchemy
# import time
import datetime


db = SQLAlchemy()


class User(db.Model):
    """
    Users Class for creating the 'users' table in the database
    and for managing user's information
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(15), nullable=False, unique=True)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.Text, nullable=False)
    terms = db.Column(db.Boolean, unique=False, default=False)
    message = db.relationship('Message', lazy='subquery', backref='user',
                              order_by='Message.id')

    def __repr__(self):
        """
        Returns the user's username when the __str__ function is called.
        """
        return f"Username:{self.username}"

    def save(self):
        """ saves user's data """
        db.session.add(self)
        db.session.commit()


class Channel(db.Model):
    """
    Channel Model for creating the 'channels' table and managing channel
    related objects
    """
    __tablename__ = 'channel'
    id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(20), nullable=False)
    messages = db.relationship('Message', lazy='dynamic', backref='channel',
                               order_by='Message.id')

    def __init__(self, name):
        self.channel_name = name

    def save(self):
        """ saves a channel and its data """
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"Channel:'{self.channel_name}'"


class Message(db.Model):
    """Message table in the database"""
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    message = db.Column(db.Text, nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'),
                           nullable=False)

    # __mapper_args__ = {
    #                 'version_id_col': timestamp,
    #                 'version_id_generator': lambda v: time.strftime('%H:%M')
    # }

    def __init__(self, message):
        self.message = message

    def save(self):
        """ saves messages """
        db.session.add(self)
        db.session.commit()


# class DM(db.model):
#     """ Direct Messages (DM) table in the database"""
#     __tablename__ = 'DM'
#     id = db.Column(db.Integer, primary_key=True)
    
