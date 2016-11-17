import pandas as  pd
import json, re
from flask import (Flask, flash, Markup, redirect, render_template, request,
                   Response, session, url_for)

from app import app, db
from .models import Tweet

tweets = pd.read_csv('tweets.csv')
# tweets = pd.read_sql('tweet', db.engine)


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

        languages = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech', 'cy': 'Welsh', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
                 'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'ht': 'Haitian', 'hu': 'Hungarian', 'hy': 'Armenian', 'id': 'Indonesian', 'in': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
                 'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
                 'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'und': 'Undetermined', 'ur': 'Urdu',
                 'vi': 'Vietnamese', 'zh': 'Chinese'}

        langs = tweets['lang'].dropna()
        langCounter = pd.DataFrame(langs.value_counts())
        langFraction = 100 * langCounter / langCounter.sum()
        langFraction = langFraction.round(3)
        langFraction.index = [languages[x] for x in langFraction.index]
        # langFraction = [tuple(x) for x in langFraction.itertuples()]
        langFraction = langFraction.drop(['English','Undetermined']).head(10)

        return langFraction


@app.route("/")
def main():
    langFraction = getLangFraction(tweets)
    return render_template("index.html", charts=charts)

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
