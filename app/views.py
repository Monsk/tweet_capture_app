from flask import Flask, render_template
import pandas as  pd

from app import app, db
from .models import Tweet

def getTZoneFraction():
        # Extract the timezones, count them, and then turn the counter dict into a list of tuples

        tweets = pd.read_sql('tweet', db.engine)

        tzones = tweets['time_zone'].dropna()
        tzoneCounter = pd.DataFrame(tzones.value_counts())
        tzoneCounts = [tuple(x) for x in tzoneCounter.itertuples()]

        tzoneFraction = 100 * tzoneCounter / tzoneCounter.sum()
        tzoneFraction = tzoneFraction.round(1)
        tzoneFraction = [tuple(x) for x in tzoneFraction.itertuples()]

        return tzoneFraction

def getLangFraction():
        # Extract the languages, count them, and then turn the counter dict into a list of tuples

        tweets = pd.read_sql('tweet', db.engine)

        languages = {'ar': 'Arabic', 'bg': 'Bulgarian', 'ca': 'Catalan', 'cs': 'Czech', 'da': 'Danish', 'de': 'German', 'el': 'Greek', 'en': 'English', 'es': 'Spanish', 'et': 'Estonian',
                 'fa': 'Persian', 'fi': 'Finnish', 'fr': 'French', 'hi': 'Hindi', 'hr': 'Croatian', 'hu': 'Hungarian', 'id': 'Indonesian', 'is': 'Icelandic', 'it': 'Italian', 'iw': 'Hebrew',
                 'ja': 'Japanese', 'ko': 'Korean', 'lt': 'Lithuanian', 'lv': 'Latvian', 'ms': 'Malay', 'nl': 'Dutch', 'no': 'Norwegian', 'pl': 'Polish', 'pt': 'Portuguese', 'ro': 'Romanian',
                 'ru': 'Russian', 'sk': 'Slovak', 'sl': 'Slovenian', 'sr': 'Serbian', 'sv': 'Swedish', 'th': 'Thai', 'tl': 'Filipino', 'tr': 'Turkish', 'uk': 'Ukrainian', 'und': 'Undetermined', 'ur': 'Urdu',
                 'vi': 'Vietnamese', 'zh_CN': 'Chinese (simplified)', 'zh_TW': 'Chinese (traditional)'}

        langs = tweets['lang'].dropna()
        langCounter = pd.DataFrame(langs.value_counts())
        langFraction = 100 * langCounter / langCounter.sum()
        langFraction = langFraction.round(3)
        langFraction.index = [languages[x] for x in langFraction.index]
        langFraction = [tuple(x) for x in langFraction.itertuples()]

        return langFraction


@app.route("/")
def main():
    return render_template("lang.html")

@app.route("/chart")
def chart():
	# The data can come from anywhere you can read it; for instance, a SQL
	# query or a file on the filesystem created by another script.
	# This example expects two values per row; for more complicated examples,
	# refer to the Google Charts gallery.

    tzoneFraction = getTZoneFraction()
    langFraction = getLangFraction()

    #Remove English from the list as it overshadows the smaller fractions
    langFraction = [i for i in langFraction if i[0] not in ('English', 'Undetermined')]

    return render_template('chart.html', **locals())
