"""Database models for the eavesdropper application."""
"""Built upon this tutorial https://jeffknupp.com/blog/2014/01/31/a-python-app-to-see-what-people-are-saying-about-you/ """

import datetime

# from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
# from sqlalchemy.orm import relationship, backref

from app import db
from app import app

class Tweet(db.Model):
    # """Table for storing relevent tweets"""
    __tablename__ = 'tweet'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tweet_id = db.Column(db.String)
    text = db.Column(db.String)
    url_link = db.Column(db.String)
    retweet_count = db.Column(db.Integer)
    retweet_text = db.Column(db.String)
    lang = db.Column(db.String)
    time_zone = db.Column(db.String)
    source = db.Column(db.String)
    geolocation = db.Column(db.String)
    user_location = db.Column(db.String)
    user_id = db.Column(db.String)
    user_screen_name = db.Column(db.String)
    source_user_id = db.Column(db.String)
    source_user_screen_name = db.Column(db.String)
    recorded_at = db.Column(db.DateTime, default=datetime.datetime.now)
    occurred_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __str__(self):
        """Return the string representation of a tweet."""
        return self.text

    def to_json(self):
        return {
                'id': self.id,
                'text': self.text,
                'user_screen_name': self.user_screen_name,
                'lang': self.lang,
                'time_zone': self.time_zone,
                'recorded_at': str(self.recorded_at),
                'occurred_at': str(self.occurred_at)}

    def __repr__(self):
        return '<Tweet {}>'.format(self.text.encode('utf-8'))
