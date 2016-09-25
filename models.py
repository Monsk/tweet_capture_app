"""Database models for the eavesdropper application."""
"""Built upon this tutorial https://jeffknupp.com/blog/2014/01/31/a-python-app-to-see-what-people-are-saying-about-you/ """

import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tweet(Base):
    """Table for storing relevent tweets"""

    __tablename__ = 'tweet'
    id = Column(Integer, primary_key=True, autoincrement=True)
    text = Column(String)
    associated_user = Column(String)
    lang = Column(String)
    time_zone = Column(String)
    recorded_at = Column(DateTime, default=datetime.datetime.now)
    occurred_at = Column(DateTime, default=datetime.datetime.now)

    def __str__(self):
        """Return the string representation of a tweet."""
        return self.text

    def to_json(self):
        return {
                'id': self.id,
                'text': self.text,
                'associated_user': self.associated_user,
                'lang': self.lang,
                'time_zone': self.time_zone,
                'recorded_at': str(self.recorded_at),
                'occurred_at': str(self.occurred_at)}

    def __repr__(self):
        return '<Tweet {}>'.format(self.text)
