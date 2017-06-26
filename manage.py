import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask.ext.migrate import Migrate, MigrateCommand

from app import app, db
from app.models import ComputedData
from twitter_stream import twitter_listener
from analysis_functions import getCommonSources, getTimeLangFraction

import datetime

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def catch_tweets():
    num_tweets_to_grab = 100

    # pdb.set_trace()
    twit = twitter_listener(num_tweets_to_grab)
    twit.get_streaming_data('brexit')

def saveComputedData(name, data):
    """
    Save the computed data as a json string in the ComputedData table
    If the data object doesn't exist, create it; otherwise, update it
    """

    if (db.session.query(ComputedData.dataTitle).filter_by(dataTitle=name).scalar() is None):
        computedData = ComputedData(
            dataTitle = name,
            jsonData = data.to_json(orient='records'),
            updated_at = datetime.datetime.now()
        )
        db.session.add(computedData)
        db.session.commit()
    else:
        computedData = ComputedData.query.filter_by(dataTitle=name).first()
        computedData.jsonData = data.to_json(orient='records')
        computedData.updated_at = datetime.datetime.now()
        db.session.commit()
    return

@manager.command
def compute_plot_data():
    saveComputedData('sourceFraction', getCommonSources(db))
    saveComputedData('timeLangFraction', getTimeLangFraction(db))


if __name__ == "__main__":
    manager.run()
