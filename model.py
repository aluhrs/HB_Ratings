from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref

import correlation

ENGINE = None
Session = None

# To create the tables from scratch change echo to True in engine
# and call this below from python -i model.py 
# Base.metadata.create_all(engine)

engine = create_engine("sqlite:///ratings.db", echo=False)
session = scoped_session(sessionmaker(bind=engine, autocommit = False, 
                                        autoflush = False))


Base = declarative_base()
Base.query = session.query_property()


### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)

    def similarity(self, other):
        u_ratings = {}
        paired_ratings = []
        for r in self.ratings:
            u_ratings[r.movie_id] = r

        for r in other.ratings:
            u_r = u_ratings.get(r.movie_id)
            if u_r:
                paired_ratings.append( (u_r.rating, r.rating) )

        if paired_ratings:
            return correlation.pearson(paired_ratings)
        else:
            return 0.0

    def predict_rating(self, movie):
        ratings = self.ratings
        other_ratings = movie.ratings
        similarities = [ (self.similarity(r.user), r) \
            for r in other_ratings ]
        similarities.sort(reverse = True)
        similarities = [ sim for sim in similarities if sim[0] > 0]
        if not similarities:
            return None
        numerator = sum([ r.rating * similarity for similarity, r in similarities ])
        denominator = sum([ similarity[0] for similarity in similarities ])
        return numerator/denominator 


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key = True)
    name = Column(String(64), nullable=True)
    released_at = Column(Date, nullable=True)
    imdb_url = Column(String(100), nullable=True)

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key = True)
    # ForeignKey is describing the relationship between the movie_id in the ratings table
    # and the id in the movies table
    movie_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer, nullable=True)
    
    # relationship is adding an attribute to the object 
    # so below, user is the child (or children) to Ratings. 
    user = relationship("User",
            backref=backref("ratings", order_by=id))
    movie = relationship("Movie",
            backref=backref("ratings", order_by=id))
        

### End class declarations
# to connect to your database type sessions = connect() in python -i model.py

def authenticate(username, password):
    authentication = session.query(User).filter_by(email = username,
                                            password = password).all()
    # print authentication
    if authentication == []:
        return False
    else:
        return True

def create_user(username, password):
    # create a new instance of the user class
    u = User(email=username, password=password)
    # add the user
    session.add(u)
    # commit the user to the database
    session.commit()



        
# def connect():
#     global ENGINE
#     global Session

#     ENGINE = create_engine("sqlite:///ratings.db", echo=True)
#     Session = sessionmaker(bind=ENGINE)

#     return Session()


def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
