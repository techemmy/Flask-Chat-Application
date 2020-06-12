import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import time 

db = SQLAlchemy()

members = db.Table('members',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('channel_id', db.Integer, db.ForeignKey('channels.id'), primary_key=True)
)

# messages = db.Table('messages',
#     db.Column('message_id', db.Integer, db.ForeignKey('message.id'), primary_key=True),
#     db.Column('channel_id', db.Integer, db.ForeignKey('channel.id'), primary_key=True),
#     db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
# )

class User(db.Model):
    """
    Users Class for creating the 'users' table in the database
    and for managing user's information
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(10), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.Text, nullable=False)
    terms = db.Column(db.Boolean, unique=False, default=False)

    def __str__(self):
        """
        Returns the user's username when the __str__ function is called.
        """
        return f"Your username is {self.username}"

    def add_user(firstname, lastname, username, email, password, terms):
        """ 
        Help: 
            add user funtion for adding a user to the user to the users table 
        Usage:
            - Make sure that the users variables are defined then pass them to 
            the function
            - You add them to the function by calling the method
                User.add_user(firstname=firstname, lastname=lastname, username=username, email=email
                              password=password, terms=terms)
        """
        new_user = User(firstname=firstname, lastname=lastname, username=username,
            email=email, password=password, terms=terms)
        db.session.add(new_user)
        db.session.commit()
        
class Channel(db.Model):
    """
    Channel Model for creating the 'channels' table and managing channel
    related objects
    """
    __tablename__ = 'channels'
    id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(20), nullable=False)
    member =  db.relationship('User', secondary=members, lazy='subquery', 
        backref=db.backref('members', lazy=True))
    messages = db.Column(db.Text, nullable=True)
    
# class Message(db.Model):
#     """
#     Message Model for storing user messages in relation to their channels and
#     the users.
#     """
#     __tablename__ = 'messages'
#     id = db.column(db.Integer, primary_key=True)
#     user_id = db.relationship('Channel')

class Msg:
    """
    Message function for adding messages to the Channel Class or channels table
    """
    def __init__(self, name, message):
        """ configure message's arguments """
        self.name = name
        self.timestamp = time.strftime('%H:%M')
        self.message = message