import pandas as  pd
import json, re
from flask import (Flask, flash, Markup, redirect, render_template, request,
                   Response, session, url_for)
from datetime import datetime, timedelta

from app import app, db
from .models import Tweet

# tweets = pd.read_csv('tweets.csv')
tweets = pd.read_sql('tweet', db.engine)

languages = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech', 'cy': 'Welsh', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian', 'eu': Basque,
         'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'ht': 'Haitian', 'hu': 'Hungarian', 'hy': 'Armenian', 'id': 'Indonesian', 'in': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
         'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
         'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'und': 'Undetermined', 'ur': 'Urdu',
         'vi': 'Vietnamese', 'zh': 'Chinese'}

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
    langFraction['language'] = [languages[x] for x in langFraction.index]
    langFraction = langFraction.rename(columns={'lang': 'percentage'})
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



@app.route("/")
def main():
    langFraction = getLangFraction(tweets)
    commonLanguages = langFraction.index
    langFraction = langFraction.to_json(orient='records')
    timeLangFraction = getTimeLangFraction(tweets, commonLanguages).to_json(orient='records')
    # print(timeLangFraction)

    return render_template("index.html", langData = langFraction, timeLangData = timeLangFraction)

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
