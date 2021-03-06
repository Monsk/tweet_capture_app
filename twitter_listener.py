import tweepy
import datetime
from tweepy.streaming import StreamListener
from tweepy import Stream
from config import *
import pdb
import json
from collections import Counter
import pprint

from app.models import Tweet
from app import db

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# engine = create_engine('sqlite:///sqlite.db')
# Session = sessionmaker(bind=engine)
# session = Session()

langs = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
         'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
         'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
         'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'und': 'Undetermined', 'uk': 'Ukrainian', 'ur': 'Urdu',
         'vi': 'Vietnamese', 'zh_CN': 'Chinese (simplified)', 'zh_TW': 'Chinese (traditional)'}

class twitter_listener(StreamListener):

    def __init__(self, num_tweets_to_grab, stats, retweet_count=10000):
        self.counter = 0
        self.num_tweets_to_grab = num_tweets_to_grab
        self.retweet_count = retweet_count
        self.stats = stats
        # self.get_tweet_html = get_tweet_html

    def on_data(self, data):
        try:
            json_data = json.loads(data)
            print(self.counter)

            pprint.pprint(json_data)

            self.counter += 1

            tweet = Tweet(
                tweet_id = json_data["id_str"],
                text = json_data["text"],
                lang = json_data["lang"],
                time_zone = json_data["user"]["time_zone"],
                source = json_data["source"],
                geolocation = json_data["geo"],
                user_location = json_data["user"]["location"],
                user_id = json_data["user"]["id_str"],
                user_screen_name = json_data["user"]["screen_name"],
                recorded_at = datetime.datetime.now(),
                occurred_at = datetime.datetime.strptime(json_data["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
                )

            if "retweeted_status" in json_data:
                # Adds retweet data if the tweet is a retweet
                tweet.retweet_count = json_data["retweeted_status"]["retweet_count"]
                tweet.retweet_text = json_data["retweeted_status"]["text"]
                tweet.source_user_id = json_data["retweeted_status"]["user"]["id_str"]
                tweet.source_user_screen_name = json_data["retweeted_status"]["user"]["screen_name"]

            for element in json_data["entities"]["urls"]:
                # @TODO: store all the urls in the list, not just the last one
                tweet.url_link = element["expanded_url"]

            try:
                db.session.add(tweet)
                db.session.commit()
                print("Tweet added to database.")
            except:
                print("Failed to add to database.")
                return False

            if self.counter >= self.num_tweets_to_grab:
                return False

            return True
        except:
            # @TODO: Very dangerous, come back to this!
            pass

    def on_error(self, status):
        print(status)
        if status == 420:
            #Disconnect the stream if exceeded connection rate limit
            return False


class TwitterMain():

    def __init__(self, num_tweets_to_grab, retweet_count):
        self.auth = tweepy.OAuthHandler(cons_key, cons_sec)
        self.auth.set_access_token(app_tok, app_sec)
        self.api = tweepy.API(self.auth)
        self.num_tweets_to_grab = num_tweets_to_grab
        self.retweet_count = retweet_count
        self.stats = stats()

    def get_streaming_data(self):
        twitter_stream = Stream(self.auth, twitter_listener(num_tweets_to_grab=self.num_tweets_to_grab, retweet_count=self.retweet_count, stats=self.stats)).filter(track=['brexit'])
        try:
            twitter_stream.sample()
        except Exception as e:
            print(e.__doc__)

        lang, top_lang, top_tweets = self.stats.get_stats()
        print(Counter(lang))
        print(Counter(top_lang))
        # print(top_tweets)

    def get_trends(self):
        trends = self.api.trends_place(1)
        print(json.dumps(trends, indent=4, sort_keys=True))
        trend_data = []

        for trend in trends[0]["trends"]:
            print(trend['name'])
            trend_tweets = []
            trend_tweets.append(trend['name'])
            search_results = tweepy.Cursor(self.api.search, q = trend['name']).items(3)

            for result in search_results:
                trend_tweets.append(self.get_tweet_html(result.id))
                # print(result[0])

            trend_data.append(tuple(trend_tweets))

        # print(trend_data)

    def get_tweet_html(self, id):
        oembed = self.api.get_oembed(id=id, hide_media = True, hide_thread = True)

        tweet_html = oembed['html'].strip("\n")

        return tweet_html


class stats():

    def __init__(self):
        self.lang = []
        self.top_lang = []
        self.top_tweets = []

    def add_lang(self, lang):
        self.lang.append(lang)

    def add_top_tweets(self, tweet_html):
        self.top_tweets.append(tweet_html)

    def add_top_lang(self, top_lang):
        self.top_lang.append(top_lang)

    def get_stats(self):
        return self.lang, self.top_lang, self.top_tweets




if __name__ == "__main__":
    num_tweets_to_grab = 10
    retweet_count = 500

    # pdb.set_trace()
    twit = TwitterMain(num_tweets_to_grab, retweet_count)
    twit.get_streaming_data()
