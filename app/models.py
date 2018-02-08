"""Database models for the eavesdropper application."""
"""Built upon this tutorial https://jeffknupp.com/blog/2014/01/31/a-python-app-to-see-what-people-are-saying-about-you/ """

import datetime
from textblob import TextBlob
import re

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
    longitude = db.Column(db.Float(10, 6))
    latitude  = db.Column(db.Float(10, 6))
    user_location = db.Column(db.String)
    user_id = db.Column(db.String)
    user_screen_name = db.Column(db.String)
    source_user_id = db.Column(db.String)
    source_user_screen_name = db.Column(db.String)
    sentiment_score = db.Column(db.Float)
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

    def clean_tweet(self):
        '''
        Utility function to clean tweet text by removing links, special characters
        using simple regex statements.
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", self.text).split())

    def remove_url(self, is_retweet):
        '''
        Utility function to clean tweet text of urls
        '''
        target_text = self.retweet_text if is_retweet else self.text
        return re.sub('https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=\/]{2,256}', '', target_text)

    def get_tweet_sentiment(self):
        '''
        Utility function to classify sentiment of passed tweet
        using textblob's sentiment method
        '''
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet())
        # set sentiment
        return analysis.sentiment.polarity

    def __repr__(self):
        return '<Tweet {}>'.format(self.text.encode('utf-8'))

class ComputedData(db.Model):
    # """Table for storing computed data that will be used for plotting"""
    __tablename__ = 'computedData'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    dataTitle = db.Column(db.String)
    jsonData = db.Column(db.String)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __str__(self):
        """Return the title of the data"""
        return self.dataTitle

    def get_json_data(self):
        return json.loads(self.jsonData)

    def __repr__(self):
        return self.dataTitle

class WordCounts(db.Model):
    # """Table for storing the time series of the frequencies of words tweeted"""
    __tablename__ = 'wordCounts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    word = db.Column(db.String)
    frequencyData = db.Column(db.String)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.now)

    def __str__(self):
        """Return the title of the data"""
        return self.word

    def get_json_data(self):
        return json.loads(self.jsonData)

    def __repr__(self):
        return self.word
