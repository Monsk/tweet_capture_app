from TwitterAPI import TwitterAPI, TwitterError
from config import *
import pprint
import datetime
from textblob import TextBlob

from app.models import Tweet
from app import db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


api = TwitterAPI(CONS_KEY, CONS_SEC, APP_TOK, APP_SEC)

# r = api.request('statuses/filter', {'track':'brexit'})
# for item in r:
#     pprint.pprint(item)

class twitter_listener():

    def __init__(self, num_tweets_to_grab):
        self.counter = 0
        self.num_tweets_to_grab = num_tweets_to_grab

    def get_streaming_data(self, tracker):
        while True:
            try:
                iterator = api.request('statuses/filter', {'track':tracker}).get_iterator()
                for item in iterator:
                    if 'text' in item:

                        print(self.counter)
                        # pprint.pprint(item)

                        self.counter += 1

                        tweet = Tweet(
                            tweet_id = item["id_str"],
                            text = item["text"],
                            lang = item["lang"],
                            time_zone = item["user"]["time_zone"],
                            source = item["source"],
                            user_location = item["user"]["location"],
                            user_id = item["user"]["id_str"],
                            user_screen_name = item["user"]["screen_name"],
                            recorded_at = datetime.datetime.now(),
                            occurred_at = datetime.datetime.strptime(item["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
                            )

                        if "retweeted_status" in item:
                            # Adds retweet data if the tweet is a retweet
                            tweet.retweet_count = item["retweeted_status"]["retweet_count"]
                            tweet.retweet_text = item["retweeted_status"]["text"]
                            tweet.source_user_id = item["retweeted_status"]["user"]["id_str"]
                            tweet.source_user_screen_name = item["retweeted_status"]["user"]["screen_name"]

                        for element in item["entities"]["urls"]:
                            # @TODO: store all the urls in the list, not just the last one
                            tweet.url_link = element["expanded_url"]

                        tweet.sentiment_score = tweet.get_tweet_sentiment()
                        print(tweet.sentiment_score)

                        try:
                            db.session.add(tweet)
                            db.session.commit()
                            print("Tweet added to database.")
                        except:
                            print("Failed to add to database.")
                            return False

                        if self.counter >= self.num_tweets_to_grab:
                            print("{} tweets caught".format(self.num_tweets_to_grab))
                            return False

                    elif 'disconnect' in item:
                        event = item['disconnect']
                        if event['code'] in [2,5,6,7]:
                            # something needs to be fixed before re-connecting
                            raise Exception(event['reason'])
                        else:
                            # temporary interruption, re-try request
                            break
            except TwitterError.TwitterRequestError as e:
                if e.status_code < 500:
                    # something needs to be fixed before re-connecting
                    raise
                else:
                    # temporary interruption, re-try request
                    pass
            except TwitterError.TwitterConnectionError:
                # temporary interruption, re-try request
                pass



if __name__ == "__main__":
    num_tweets_to_grab = 100

    # pdb.set_trace()
    twit = twitter_listener(num_tweets_to_grab)
    twit.get_streaming_data('brexit')
