from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from tweeter import application

db = SQLAlchemy(app=application)

class BaseModel(object):
    """ The default parameter definiton class """
    active = db.Column(db.Boolean, default=True)
    deleted = db.Column(db.Boolean, default=False)
    created_time = db.Column(db.DateTime(), default=datetime.now())

    def delete(self):
        """standard delete method for all inherited classes"""
        self.deleted = True


class KeyWords(db.Model, BaseModel):
    """The table structure of the keyword streams"""
    id = db.Column(db.Integer, primary_key=True)
    streams = db.Column(db.Text)

    def __init__(self, streams=''):
        self.streams = streams

    def __repr__(self):
        return "%s" % self.streams

    def deactivate(self):
        """deactivates a keyword stream"""
        self.active = False

class Tweets(db.Model, BaseModel):
    """The table structure of the tweets"""
    id = db.Column(db.Integer, primary_key=True)
    keywords_id = db.Column(db.Integer, db.ForeignKey('key_words.id'))

    tweet_generated_time = db.Column(db.DateTime())
    twitter_user = db.Column(db.String(100))
    tweet = db.Column(db.Text)

    key_words = db.relationship('KeyWords', backref=db.backref('tweets', lazy='dynamic'))

    # def __init__(self, user, tweet):
    #     self.streams = streams

    def __repr__(self):
        return "%s" % self.twitter_user
