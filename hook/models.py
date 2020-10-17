#!usr/bin/env python
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.expression import or_, and_
from sqlalchemy.exc import IntegrityError
# import time
import datetime
import os


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
        Returns the user's username when the __repr__ function is called.
        """
        return f"Username:{self.username}"

    def save(self):
        """ saves user's data """
        db.session.add(self)
        db.session.commit()

    def get_dm(self):
        dms = Dm.query.filter(or_(
                                Dm.user_one == self.id,
                                Dm.user_two == self.id)).all()
        output = []
        for dm in dms:
            output.append([dm.id, dm.get_name(self.id), dm.room])

        return output


class Channel(db.Model):
    """
    Channel Model for creating the 'channels' table and managing channel
    related objects
    """
    __tablename__ = 'channel'
    id = db.Column(db.Integer, primary_key=True)
    channel_name = db.Column(db.String(20), nullable=False, unique=True)
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    message = db.Column(db.Text, nullable=False)
    channel_id = db.Column(db.Integer, db.ForeignKey('channel.id'),
                           nullable=True)
    dm_id = db.Column(db.Integer, db.ForeignKey('dm.id'), nullable=True)

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


class Dm(db.Model):
    """ DM table in the database """
    __tablename__ = 'dm'
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.Text, unique=True)
    user_one = db.Column(db.Integer, nullable=False)
    user_two = db.Column(db.Integer, nullable=False)
    messages = db.relationship('Message', backref='direct_msg',
                               lazy='dynamic', order_by='Message.timestamp')

    def __init__(self, u1, u2):
        self.user_one = u1
        self.user_two = u2
        self.room = self._get_room()
        if self._validate_dm():
            self.save()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

    def _get_room(self):
        run = True
        while run:
            room = os.urandom(16)
            for dm in Dm.query.all():
                if room != dm.room:
                    run = False
        return room

    def get_name(self, present_user_id):
        try:
            users = [User.query.get(self.user_one),
                     User.query.get(self.user_two)]
            for i in users:
                if i.id != present_user_id:
                    other_user = i.username

            return other_user if other_user else None
        except Exception as e:
            raise e

    def _validate_dm(self):
        user1 = self.user_one
        user2 = self.user_two
        exists = Dm.query.filter(or_(
                            and_(Dm.user_one == user1,
                                 Dm.user_two == user2),
                            and_(Dm.user_one == user2,
                                 Dm.user_two == user1))).all()
        if exists:
            raise Exception("DM already exists.")
            return False
        return True
