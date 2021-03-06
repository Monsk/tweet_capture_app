import os
from flask import Flask, render_template
# from werkzeug.contrib.cache import MemcachedCache

from flask_sqlalchemy import SQLAlchemy
import sys
import logging


# Create a Flask WSGI app and configure it using values from the module, and secret keys from instance/config.
app = Flask(__name__)
app.config.from_object('config')

app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

db = SQLAlchemy(app)

from app import views, models

if os.environ.get('HEROKU') is not None:
    import logging
    stream_handler = logging.StreamHandler()
    app.logger.addHandler(stream_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('website startup')
    app.config['CACHE_TYPE'] = 'saslmemcached'
    app.config.setdefault('CACHE_MEMCACHED_SERVERS',
            [os.environ['MEMCACHIER_SERVERS']])
    app.config.setdefault('CACHE_MEMCACHED_USERNAME',
            os.environ['MEMCACHIER_USERNAME'])
    app.config.setdefault('CACHE_MEMCACHED_PASSWORD',
            os.environ['MEMCACHIER_PASSWORD'])
    cache = Cache(app, app.config)
