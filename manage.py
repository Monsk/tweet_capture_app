from flask_script import Manager

from app import app
from twitter_listener import TwitterMain

manager = Manager(app)

@manager.command
def catch_tweets():
    num_tweets_to_grab = 100
    retweet_count = 500
    twit = TwitterMain(num_tweets_to_grab, retweet_count)
    twit.get_streaming_data()

if __name__ == "__main__":
    manager.run()
