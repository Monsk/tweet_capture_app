import pandas as  pd
import json, re
from flask import (Flask, flash, Markup, redirect, render_template, request,
                   Response, session, url_for)
from datetime import datetime, timedelta

from app import app, db
from .models import Tweet, ComputedData

from analysis_functions import getSentimentScores

# tweets = pd.read_csv('tweets.csv')
# tweets = pd.read_sql('tweet', db.engine)

def getTZoneFraction(tweets):
    # Extract the timezones, count them, and then turn the counter dict into a list of tuples

    tzones = pd.read_sql_query("SELECT time_zone from Tweet", db.engine).iloc[:,0].dropna()
    tzoneCounter = pd.DataFrame(tzones.value_counts())
    tzoneCounts = [tuple(x) for x in tzoneCounter.itertuples()]

    tzoneFraction = 100 * tzoneCounter / tzoneCounter.sum()
    tzoneFraction = tzoneFraction.round(1)
    tzoneFraction = [tuple(x) for x in tzoneFraction.itertuples()]

    return tzoneFraction

@app.route("/_string_filter", methods=['GET', 'POST'])
def _string_filter():
    kw = lambda x: timedelta(days=x.weekday())
    stringArray = json.loads(request.args.get('str_arr'))
    stringArray = filter(None, stringArray)
    combinedStringStats = pd.DataFrame()

    tweets = pd.read_sql_query("SELECT text, occurred_at from Tweet", db.engine)
    tweets.occurred_at = pd.DatetimeIndex(tweets.occurred_at).normalize()
    tweets['occurred_at_week'] = tweets.occurred_at - tweets.occurred_at.map(kw)
    sumTweets = tweets.groupby(tweets['occurred_at_week']).text.count()

    for string in stringArray:
        filterTweets = tweets[tweets.text.str.contains(string, case=False)]
        wordCounts = filterTweets.groupby(filterTweets['occurred_at_week']).text.count()
        wordCounts = wordCounts.reset_index()
        sumTweets = sumTweets.reset_index()

        wordSummary = wordCounts.merge(sumTweets, left_on='occurred_at_week', right_on='occurred_at_week')
        wordSummary = wordSummary.rename(columns={'text_x': 'count', 'text_y': 'sum'})
        wordSummary['percentage'] = (100 * wordSummary['count'] / wordSummary['sum']).round(2)
        wordSummary.occurred_at_week = wordSummary.occurred_at_week.dt.strftime('%d %b %Y')
        wordSummary['string'] = string
        combinedStringStats = combinedStringStats.append(wordSummary)

    return combinedStringStats.to_json(orient='records')


@app.route("/")
def main():

    timeLangFraction = ComputedData.query.filter_by(dataTitle='timeLangFraction').first().jsonData
    sourceFraction = ComputedData.query.filter_by(dataTitle='sourceFraction').first().jsonData
    sentimentData = ComputedData.query.filter_by(dataTitle='sentimentScore').first().jsonData

    return render_template("index.html",
    timeLangData = timeLangFraction,
    sourceData = sourceFraction,
    sentimentData = sentimentData
    )

@app.route("/about")
def about():
    tweet_count = db.session.query(Tweet).count()
    return render_template("about.html", tweet_count = tweet_count)
