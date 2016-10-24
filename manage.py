import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import app, db
from twitter_listener import TwitterMain, twitter_listener

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def catch_tweets():
    num_tweets_to_grab = 100
    retweet_count = 500

    twit = TwitterMain(num_tweets_to_grab, retweet_count)
    twit.get_streaming_data()

if __name__ == "__main__":
    manager.run()
