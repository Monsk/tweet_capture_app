import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import load_only
from flask_script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import app, db
from app.models import ComputedData, Tweet, WordCounts
from twitter_stream import twitter_listener
from analysis_functions import getCommonSources, getTimeLangFraction, getSentimentScores, getTweetCountByCommonSources
from textblob import TextBlob

from collections import Counter
import re, string, json

import datetime
from datetime import timedelta

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def catch_tweets():
    num_tweets_to_grab = 100

    # pdb.set_trace()
    twit = twitter_listener(num_tweets_to_grab)
    twit.get_streaming_data('brexit')

def saveComputedData(name, data):
    """
    Save the computed data as a json string in the ComputedData table
    If the data object doesn't exist, create it; otherwise, update it
    """
    # If object doesn't exist, create
    if (db.session.query(ComputedData.dataTitle).filter_by(dataTitle=name).scalar() is None):
        computedData = ComputedData(
            dataTitle = name,
            jsonData = data
        )
        db.session.add(computedData)
        db.session.commit()
    # If object does exist, update
    else:
        computedData = ComputedData.query.filter_by(dataTitle=name).first()
        computedData.jsonData = data
        computedData.updated_at = datetime.datetime.now()
        db.session.commit()
    return

@manager.command
def compute_plot_data():
    saveComputedData('sourceFraction', getCommonSources(db))
    saveComputedData('timeLangFraction', getTimeLangFraction(db))
    saveComputedData('sentimentScore', getSentimentScores(db))
    saveComputedData('tweetCountByCommonSources', getTweetCountByCommonSources(db))

@manager.command
def compute_sentiment_scores():
    n=0
    tableRows = db.session.query(Tweet).count()
    batchSize = 1000
    print(tableRows)
    for n in xrange(0, tableRows, batchSize):
        print(n)
        for tweet in db.session.query(Tweet)[n:n+batchSize-1]:
            if tweet.sentiment_score is None:
                tweet.sentiment_score = tweet.get_tweet_sentiment()
        db.session.commit()


@manager.command
def count_tweet_words(today = None, day_scope = None):

    if day_scope is None:
        if today is None:
            today = datetime.datetime.now()
        scoped_tweets = db.session.query(Tweet).filter( Tweet.recorded_at > today - timedelta(days=1) )
    elif day_scope is not None and today is not None:
        scoped_tweets = db.session.query(Tweet).filter( Tweet.recorded_at > today - timedelta(days=day_scope) and Tweet.recorded_at < today)
    else:
        print("Insufficient information to scope tweets")
        return

    combined_string = ''

    for tweet in scoped_tweets:
        # select retweet_text if the text is a retweet
        if tweet.retweet_text is None:
            combined_string = combined_string + tweet.remove_url(is_retweet = False)
        else:
            combined_string = combined_string + tweet.remove_url(is_retweet = True)

    # remove all punctuation and convert to lower case
    combined_string = re.sub('([^\s\w]|_)+', '', combined_string.lower())
    word_counts = sorted(Counter(combined_string.split()).items())
    print(len(word_counts))

    existing_words = db.session.query(WordCounts.word)
    n=0
    for word_count in word_counts:
        word = word_count[0]

        # if the word does not exist in the table, add it
        try:
            if (db.session.query(WordCounts.word).filter_by(word=word).scalar() is None):
                new_word = WordCounts(
                    word = word,
                    frequencyData = json.dumps([{'date':today.strftime("%Y-%m-%d"), 'count':word_count[1]}])
                )
                db.session.add(new_word)
            else:
                wordCount = WordCounts.query.filter_by(word=word).first()

                if bool(re.search(today.strftime("%Y-%m-%d"), wordCount.frequencyData)):
                # Check for an entry from today already recorded
                    continue
                else:
                # If no record from today, add one
                    frequencyData = json.loads(wordCount.frequencyData)
                    frequencyData.append({'date':today.strftime("%Y-%m-%d"), 'count':word_count[1]})
                    wordCount.frequencyData = json.dumps(frequencyData)
        except:
            print(word)
    db.session.commit()
    return

@manager.command
def batch_word_count():
    # Find earliest tweet
    # For all time, in batches of 7 days, count_tweet_words
    return

@manager.command
def topSources():
    print(getTweetCountByCommonSources(db))

if __name__ == "__main__":
    manager.run()
