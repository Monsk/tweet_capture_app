import os

basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'sqlite.db') +
                               '?check_same_thread=False')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

CONS_KEY = 'vIU2HWFITKPVgK8i3IDuZqKiY'
CONS_SEC = 'METFTMQRs4QTdsR3jhO0CgoABUPK4SP7QiufwibZCoo5R4ZJV1'

APP_TOK = '610777784-EVHHlCBUR6aNTw1gcDpCma8nUvP8GROGUAQrawNz'
APP_SEC = 'iLjD2b4WO5vlS4d6eAXFj0npyMplR3yJY3le2d4pKlkAb'
