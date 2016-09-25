import os

basedir = os.path.abspath(os.path.dirname(__file__))

if os.environ.get('DATABASE_URL') is None:
    SQLALCHEMY_DATABASE_URI = ('sqlite:///' + os.path.join(basedir, 'sqlite.db') +
                               '?check_same_thread=False')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

cons_key = 'vIU2HWFITKPVgK8i3IDuZqKiY'
cons_sec = 'METFTMQRs4QTdsR3jhO0CgoABUPK4SP7QiufwibZCoo5R4ZJV1'

app_tok = '610777784-EVHHlCBUR6aNTw1gcDpCma8nUvP8GROGUAQrawNz'
app_sec = 'iLjD2b4WO5vlS4d6eAXFj0npyMplR3yJY3le2d4pKlkAb'
