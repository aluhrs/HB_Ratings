from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

Base = declarative_base()
engine = create_engine("sqlite:///ratings.db", echo=True)
# Call this below from python -i model.py when creating the tables
# Base.metadata.create_all(engine)

### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)

class Movies(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable=True)
    released_at = Column(DateTime, nullable=True)
    imdb_url = Column(String(100), nullable=True)

class Ratings(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    movie_id = Column(Integer, nullable = True)
    user_id = Column(Integer, nullable = True)
    rating = Column(Integer, nullable = True)
    
        

### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
