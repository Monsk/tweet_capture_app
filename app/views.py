from flask import Flask, render_template

from app import app, db

@app.route("/")
def main():
    return render_template("lang.html")

@app.route("/top_tweets")
def top_tweets():
    return render_template("top_tweets.html")

@app.route("/trends")
def trends():
    return render_template("trends.html")
