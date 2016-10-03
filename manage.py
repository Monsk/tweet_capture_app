import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager

from app import app
from twitter_listener import TwitterMain

manager = Manager(app)

@manager.command
def catch_tweets():
    num_tweets_to_grab = 100
    retweet_count = 500

    app = Flask(__name__)
    app.config.from_object('config')
    db = SQLAlchemy(app)

    twit = TwitterMain(num_tweets_to_grab, retweet_count)
    twit.get_streaming_data()

if __name__ == "__main__":
    manager.run()
