from sqlalchemy import create_engine
from models import Tweet, Base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///sqlite.db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)
session = Session()

m = Tweet(id=1, text='simon test tweet', associated_user='simonhunter28', lang='en', time_zone='London')
session.add(m)
session.commit()
