import pandas as pd
import json
from datetime import timedelta
from app.models import Tweet

with open('app/languages.json') as data_file:
    languages = json.load(data_file)

with open('app/euro_languages.json') as data_file:
    euro_languages = json.load(data_file)


def returnTopSources(db, count = None):
    """
    Returns the top Brexit tweeters, where count is the number to return
    """
    sources = pd.read_sql_query("SELECT source_user_screen_name from Tweet", db.engine).iloc[:,0].dropna()
    sourceCounter = pd.DataFrame(sources.value_counts())
    if count is not None:
        sourceCounter = sourceCounter.head(count)
    return sourceCounter

def getCommonSources(db):
    """
    Extract the tweet sources, count them, and then turn the counter dict into a list of tuples
    """

    print('calculating sourceFraction')
    sourceCounter = returnTopSources(db)
    sourceFraction = 100 * sourceCounter / sourceCounter.sum()
    sourceFraction = sourceFraction.round(3)
    sourceFraction = sourceFraction.reset_index()
    sourceFraction = sourceFraction.rename(columns={'source_user_screen_name': 'percentage', 'index': 'source'})

    sourceFraction = sourceFraction.head(10).to_json(orient='records')

    return sourceFraction

def getTweetCountByCommonSources(db):
    """
    Filter all tweets by authors identified by getCommonSources, count by months
    Returns a json object with each node of the format {author: xx, month: xx, tweet_count: xx}
    """

    print('calculating TweetCountByCommonSources')

    # Load tweets from database
    topSources = returnTopSources(db, 6).reset_index()['index'].values
    query_obj = db.session.query(Tweet). \
        filter(Tweet.source_user_screen_name.in_((topSources))). \
        with_entities(Tweet.source_user_screen_name, Tweet.text, Tweet.occurred_at)
    tweets = pd.read_sql(query_obj.statement, query_obj.session.bind)

    # Tidy up the timestamp and group by month
    tweets.occurred_at = pd.DatetimeIndex(tweets.occurred_at).normalize()
    tweets['occurred_at_month'] = tweets.occurred_at.dt.strftime('%b %Y')
    groupTweets = tweets.groupby([tweets['occurred_at_month'], 'source_user_screen_name']).source_user_screen_name.count()
    groupTweets.rename('count', inplace=True)
    groupTweets = groupTweets.reset_index()

    groupTweets = groupTweets.to_json(orient="records")

    return groupTweets



def getLangFraction(db):
    """
    Extract the languages, count them, and then turn the counter dict into a list of tuples
    """

    print('calculating langFraction')
    langs = pd.read_sql_query("SELECT lang from Tweet", db.engine).iloc[:,0].dropna()
    langs = langs[langs.isin(euro_languages.keys())]
    langCounter = pd.DataFrame(langs.value_counts())
    langFraction = 100 * langCounter / langCounter.sum()
    langFraction = langFraction.round(3)
    # Convert iso codes into language names
    langFraction['language'] = [languages[x] for x in langFraction.index]
    langFraction = langFraction.rename(columns={'lang': 'percentage'})
    # Remove English and undefined languages, return the top 10 remaining
    langFraction = langFraction[~langFraction.index.isin(['en','und'])].head(5)

    return langFraction

def getTimeLangFraction(db):
    """
    Looks only at European languages and creates a time series of frequency.
    Returns on the most common languages as defined in getLangFraction
    """

    def percentage(x):
        percentage = 100 * float(x['count']) / float(ggTweets[ggTweets.index == x["occurred_at_month"]][0])
        return round(percentage, 3)

    langFraction = getLangFraction(db)
    commonLanguages = langFraction.index

    tweets = pd.read_sql_query("SELECT lang, occurred_at from Tweet", db.engine)
    tweets = tweets[tweets['lang'].isin(euro_languages.keys())]
    tweets.occurred_at = pd.DatetimeIndex(tweets.occurred_at).normalize()
    tweets['occurred_at_month'] = tweets.occurred_at.dt.strftime('%b %Y')
    groupTweets = tweets.groupby([tweets['occurred_at_month'], 'lang']).lang.count()
    groupTweets.rename('count', inplace=True)
    groupTweets = groupTweets.reset_index()
    groupTweets['language'] = [languages[x] for x in groupTweets.lang]

    ggTweets = groupTweets.groupby('occurred_at_month')['count'].sum()

    groupTweets['percentage'] = groupTweets.apply(percentage, axis=1)
    # groupTweets.occurred_at_month = groupTweets.occurred_at_month.dt.strftime('%d %b %Y')
    timeLangFraction = groupTweets[groupTweets.lang.isin(commonLanguages)]

    timeLangFraction = timeLangFraction.to_json(orient='records')
    return timeLangFraction

def getSentimentScores(db):

    print('calculating sentimentScores')
    sentiment_scores = pd.read_sql_query("SELECT sentiment_score, occurred_at from Tweet", db.engine)
    sentiment_scores.occurred_at = pd.DatetimeIndex(sentiment_scores.occurred_at).normalize()
    sentiment_scores['occurred_at_month'] = sentiment_scores.occurred_at.dt.strftime('%b %Y')
    sentiment_scores.rename(index=str, columns={"sentiment_score": "Score", "occurred_at_month": "Date"}, inplace=True)

    monthScores = sentiment_scores.groupby('Date')['Score'].mean()
    monthScores = monthScores.reset_index()

    # Convert to json
    monthScores = monthScores.to_json(orient='records')
    # individualScores = sentiment_scores.to_json(orient='records')

    # sentiment_scores = str([{"monthScores": monthScores, "individualScores": individualScores}])

    return monthScores
