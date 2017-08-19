import pandas as pd
import json
from datetime import timedelta

with open('app/languages.json') as data_file:
    languages = json.load(data_file)

with open('app/euro_languages.json') as data_file:
    euro_languages = json.load(data_file)

def getCommonSources(db):
    """
    Extract the tweet sources, count them, and then turn the counter dict into a list of tuples
    """

    print('calculating sourceFraction')
    sources = pd.read_sql_query("SELECT source_user_screen_name from Tweet", db.engine).iloc[:,0].dropna()
    sourceCounter = pd.DataFrame(sources.value_counts())
    sourceFraction = 100 * sourceCounter / sourceCounter.sum()
    sourceFraction = sourceFraction.round(3)
    sourceFraction = sourceFraction.reset_index()
    sourceFraction = sourceFraction.rename(columns={'source_user_screen_name': 'percentage', 'index': 'source'})
    sourceFraction = sourceFraction.head(10)

    sourceFraction = sourceFraction.to_json(orient='records')

    return sourceFraction

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

    kw = lambda x: timedelta(days=x.weekday())
    def percentage(x):
        percentage = 100 * float(x['count']) / float(ggTweets[ggTweets.index == x["occurred_at_week"]][0])
        return round(percentage, 3)

    langFraction = getLangFraction(db)
    commonLanguages = langFraction.index

    tweets = pd.read_sql_query("SELECT lang, occurred_at from Tweet", db.engine)
    tweets = tweets[tweets['lang'].isin(euro_languages.keys())]
    tweets.occurred_at = pd.DatetimeIndex(tweets.occurred_at).normalize()
    tweets['occurred_at_week'] = tweets.occurred_at - tweets.occurred_at.map(kw)
    groupTweets = tweets.groupby([tweets['occurred_at_week'], 'lang']).lang.count()
    groupTweets.rename('count', inplace=True)
    groupTweets = groupTweets.reset_index()
    groupTweets['language'] = [languages[x] for x in groupTweets.lang]

    ggTweets = groupTweets.groupby('occurred_at_week')['count'].sum()

    groupTweets['percentage'] = groupTweets.apply(percentage, axis=1)
    groupTweets.occurred_at_week = groupTweets.occurred_at_week.dt.strftime('%d %b %Y')
    timeLangFraction = groupTweets[groupTweets.lang.isin(commonLanguages)]

    timeLangFraction = timeLangFraction.to_json(orient='records')
    return timeLangFraction

def getSentimentScores(db):
    kw = lambda x: timedelta(days=x.weekday())

    print('calculating sentimentScores')
    sentiment_scores = pd.read_sql_query("SELECT sentiment_score, occurred_at from Tweet", db.engine)
    sentiment_scores.occurred_at = pd.DatetimeIndex(sentiment_scores.occurred_at).normalize()
    sentiment_scores['occurred_at_week'] = sentiment_scores.occurred_at - sentiment_scores.occurred_at.map(kw)
    sentiment_scores.occurred_at_week = sentiment_scores.occurred_at_week.dt.strftime('%d %b %Y')
    sentiment_scores.rename(index=str, columns={"sentiment_score": "Score", "occurred_at_week": "Date"}, inplace=True)

    weekScores = sentiment_scores.groupby('Date')['Score'].mean()
    # weekScores.rename('Score', inplace=True)
    weekScores = weekScores.reset_index()
#     weekScores['individual_scores'] = ''

#     for week in weekScores.occurred_at_week:
#         # Cast individual scores into an array to store in the weekScores dataframe
#         individual_scores = sentiment_scores.sentiment_score[sentiment_scores.occurred_at_week == week].values
#         dfRow = weekScores.loc[weekScores.occurred_at_week == week].index[0]
#         weekScores.set_value(dfRow, 'individual_scores', individual_scores)

    # Convert to json
    weekScores = weekScores.to_json(orient='records')
    individualScores = sentiment_scores.to_json(orient='records')

    sentiment_scores = str([{"weekScores": weekScores, "individualScores": individualScores}])

    return sentiment_scores
