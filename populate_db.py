from sqlalchemy import create_engine
from app.models import Tweet
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///sqlite.db')
Session = sessionmaker(bind=engine)
session = Session()

m = Tweet(tweet_id=1, text='simon test tweet', user_screen_name='simonhunter28', lang='en', time_zone='London')
session.add(m)
session.commit()
