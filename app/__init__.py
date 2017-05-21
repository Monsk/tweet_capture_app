import os
from flask import Flask, render_template
# from werkzeug.contrib.cache import MemcachedCache
from flask_cache import Cache
# import pylibmc
from flask_sqlalchemy import SQLAlchemy
import sys
import logging


# Create a Flask WSGI app and configure it using values from the module, and secret keys from instance/config.
app = Flask(__name__)
app.config.from_object('config')

app.config['CACHE_TYPE'] = 'memcached'
app.config.setdefault('CACHE_MEMCACHED_SERVERS',
        ['mc3.dev.eu.ec2.memcachier.com:11211'])
app.config.setdefault('CACHE_MEMCACHED_USERNAME',
        '106E96')
app.config.setdefault('CACHE_MEMCACHED_PASSWORD',
        '6D67CCAB7F19976F6345C88F0D8AD507')

cache = Cache(app, app.config)

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
