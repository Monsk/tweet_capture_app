import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


# Create a Flask WSGI app and configure it using values from the module.
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('website startup')
