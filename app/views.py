import pandas as  pd
import json, re
from flask import (Flask, flash, Markup, redirect, render_template, request,
                   Response, session, url_for)
from datetime import datetime, timedelta

from app import app, db
from .models import Tweet

tweets = pd.read_csv('tweets.csv')
# tweets = pd.read_sql('tweet', db.engine)

with open('app/languages.json') as data_file:
    languages = json.load(data_file)

def getTZoneFraction(tweets):
    # Extract the timezones, count them, and then turn the counter dict into a list of tuples

    tzones = tweets['time_zone'].dropna()
    tzoneCounter = pd.DataFrame(tzones.value_counts())
    tzoneCounts = [tuple(x) for x in tzoneCounter.itertuples()]

    tzoneFraction = 100 * tzoneCounter / tzoneCounter.sum()
    tzoneFraction = tzoneFraction.round(1)
    tzoneFraction = [tuple(x) for x in tzoneFraction.itertuples()]

    return tzoneFraction

def getLangFraction(tweets):
    # Extract the languages, count them, and then turn the counter dict into a list of tuples
    langs = tweets['lang'].dropna()
    langCounter = pd.DataFrame(langs.value_counts())
    langFraction = 100 * langCounter / langCounter.sum()
    langFraction = langFraction.round(3)
    # Convert iso codes into language names
    langFraction['language'] = [languages[x] for x in langFraction.index]
    langFraction = langFraction.rename(columns={'lang': 'percentage'})
    # Remove English and undefined languages, return the top 10 remaining
    langFraction = langFraction[~langFraction.index.isin(['en','und'])].head(10)

    return langFraction

def getTimeLangFraction(tweets, commonLanguages):
    kw = lambda x: timedelta(days=x.weekday())
    def percentage(x):
        percentage = 100 * float(x['count']) / float(ggTweets[ggTweets.index == x["occurred_at_week"]][0])
        return round(percentage, 3)

    tweets.occurred_at = pd.DatetimeIndex(tweets.occurred_at).normalize()
    tweets['occurred_at_week'] = tweets.occurred_at - tweets.occurred_at.map(kw)
    groupTweets = tweets.groupby([tweets['occurred_at_week'], 'lang']).lang.count()
    groupTweets.rename('count', inplace=True)
    groupTweets = groupTweets.reset_index()
    groupTweets['language'] = [languages[x] for x in groupTweets.lang]

    ggTweets = groupTweets.groupby('occurred_at_week')['count'].sum()

    groupTweets['percentage'] = groupTweets.apply(percentage, axis=1)
    groupTweets.occurred_at_week = groupTweets.occurred_at_week.dt.strftime('%d %b %Y')
    groupTweets = groupTweets[groupTweets.lang.isin(commonLanguages)]
    return groupTweets

def getCommonSources(tweets):
    # Extract the tweet sources, count them, and then turn the counter dict into a list of tuples
    sources = tweets['source_user_screen_name'].dropna()
    sourceCounter = pd.DataFrame(sources.value_counts())
    sourceFraction = 100 * sourceCounter / sourceCounter.sum()
    sourceFraction = sourceFraction.round(3)
    sourceFraction = sourceFraction.reset_index()
    sourceFraction = sourceFraction.rename(columns={'source_user_screen_name': 'percentage', 'index': 'source'})
    sourceFraction = sourceFraction.head(10)
    return sourceFraction

@app.route("/_string_filter", methods=['GET'])
def getWordFrequency():
    kw = lambda x: timedelta(days=x.weekday())
    stringFilter = request.args.get('string', '', type=str)

    datedTweets = tweets
    datedTweets.occurred_at = pd.DatetimeIndex(datedTweets.occurred_at).normalize()
    datedTweets['occurred_at_week'] = datedTweets.occurred_at - datedTweets.occurred_at.map(kw)
    sumTweets = datedTweets.groupby(datedTweets['occurred_at_week']).text.count()
    filterTweets = datedTweets[datedTweets.text.str.contains(stringFilter)]
    wordCounts = filterTweets.groupby(filterTweets['occurred_at_week']).text.count()

    wordCounts = wordCounts.reset_index()
    sumTweets = sumTweets.reset_index()

    wordSummary = wordCounts.merge(sumTweets, left_on='occurred_at_week', right_on='occurred_at_week')
    wordSummary = wordSummary.rename(columns={'text_x': 'count', 'text_y': 'sum'})
    wordSummary['percentage'] = (100 * wordSummary['count'] / wordSummary['sum']).round(2)
    wordSummary.occurred_at_week = wordSummary.occurred_at_week.dt.strftime('%d %b %Y')
    wordSummary['string'] = stringFilter
    print(wordSummary.to_json(orient='records'))
    return wordSummary.to_json(orient='records')


@app.route("/")
def main():
    inputString = request.args.get('a', 0, type=int)

    langFraction = getLangFraction(tweets)
    commonLanguages = langFraction.index
    sourceFraction = getCommonSources(tweets).to_json(orient='records')
    # wordFrequency = getWordFrequency(tweets, 'brexit').to_json(orient='records')
    timeLangFraction = getTimeLangFraction(tweets, commonLanguages).to_json(orient='records')

    langFraction = langFraction.to_json(orient='records')
    topSources = json.loads(sourceFraction)
    # print(wordFrequency)
    # print(timeLangFraction)

    return render_template("index.html", langData = langFraction,
    timeLangData = timeLangFraction,
    sourceData = sourceFraction,
    topSources = topSources
    )
    # stringMatchData = wordFrequency)


@app.route("/chart")
def chart():
	# The data can come from anywhere you can read it; for instance, an SQL
	# query or a file on the filesystem created by another script.
	# This example expects two values per row; for more complicated examples,
	# refer to the Google Charts gallery.

    tzoneFraction = getTZoneFraction(tweets)
    langFraction = getLangFraction(tweets)

    #Remove English from the list as it overshadows the smaller fractions, then truncate to 10 items
    # langFraction = [i for i in langFraction if i[0] not in ('English', 'Undetermined')]
    # del langFraction[10:]

    return render_template('chart.html', **locals())
