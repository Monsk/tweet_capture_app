from flask import Flask, render_template
from collections import Counter

from app import app, db
from .models import Tweet

@app.route("/")
def main():
    return render_template("lang.html")

@app.route("/top_tweets")
def top_tweets():
    return render_template("top_tweets.html")

@app.route("/trends")
def trends():
    return render_template("trends.html")

@app.route("/chart")
def chart():
	# The data can come from anywhere you can read it; for instance, a SQL
	# query or a file on the filesystem created by another script.
	# This example expects two values per row; for more complicated examples,
	# refer to the Google Charts gallery.
    query = db.session.query(Tweet).all()
    # Extract the timezones, count them, and then turn the counter dict into a list of tuples
    timeZoneData = Counter([str(i.time_zone) for i in query]).items()
    timeZoneData = sorted(timeZoneData, key=lambda x: x[1], reverse=True)
    return render_template('chart.html', data=timeZoneData)
