import os
from flask import Flask, render_template
# from werkzeug.contrib.cache import MemcachedCache
import pylibmc
from flask_sqlalchemy import SQLAlchemy
import sys
import logging


# Create a Flask WSGI app and configure it using values from the module, and secret keys from instance/config.
app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')

cache = pylibmc.Client(["127.0.0.1:11211"], binary=True)

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
    cache = pylibmc.Client(os.environ.get('MEMCACHIER_SERVERS', '').split(','),
                        binary=True,
                        username=os.environ.get('MEMCACHIER_USERNAME', ''),
                        password=os.environ.get('MEMCACHIER_PASSWORD', ''),
                        behaviors={
                          # Faster IO
                          "tcp_nodelay": True,

                          # Keep connection alive
                          'tcp_keepalive': True,

                          # Timeout for set/get requests
                          'connect_timeout': 2000, # ms
                          'send_timeout': 750 * 1000, # us
                          'receive_timeout': 750 * 1000, # us
                          '_poll_timeout': 2000, # ms

                          # Better failover
                          'ketama': True,
                          'remove_failed': 1,
                          'retry_timeout': 2,
                          'dead_timeout': 30,
                        })
