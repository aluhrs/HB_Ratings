import model
import csv
import re
import datetime

def load_users(session):
    # open the u.users data 
    with open("seed_data/u.user") as f:
        # read the data and tokenize by |
        data = csv.reader(f, delimiter = "|")
        # looking line by line
        for line in data:
            # this tuple is akin to id = row[0], age = row[1], zipcode = row[4]
            id, age, gender, occupation, zipcode = line
            # set as integer
            id = int(id)
            # set as integer
            age = int(age)
            # creating an object
            u = model.User(id=id, email=None, password=None, age=age, zipcode=zipcode)
            # add to the session
            session.add(u)
            # commit
        session.commit()
        print "Your users have been added to the database!"            


def load_movies(session):
    # use u.item
    with open("seed_data/u.item") as f:
        # read the data and tokenize by |
        data = csv.reader(f, delimiter = "|")
        # looking line by line
        for line in data:
            # pull out the relevant elements from line and set to variables
            id = line[0]
            title = line[1]
            release_date = line[2]
            imdb = line[4]
            id = int(id)
            # account for accent marks
            title = title.decode("latin-1")
            # remove the year date at the end of the title
            title = re.sub("\(\d{4}\)","",title)
            # check for a release date, if none throw away that data
            if not release_date:
                # will bring you to the beginning of the for loop
                continue
            # set the release date to datetime
            release_date = datetime.datetime.strptime(release_date, "%d-%b-%Y")
            # create the object
            m = model.Movies(id=id, name=title, released_at=release_date, 
                                imdb_url=imdb)
            # add to the session
            session.add(m)
            # commit
        session.commit()
        print "The movies have been added!"



def load_ratings(session):
    # use u.data
    with open("seed_data/u.data") as f:
        data = csv.reader(f, delimiter = "\t")
        for line in data:
            # pull out the relevant elements from line and set to variables
            user_id, movie_id, rating, timestamp = line
            user_id = int(user_id)
            movie_id = int(movie_id)
            rating = int(rating)
            
            # create the object

            r = model.Ratings(user_id=user_id, movie_id=movie_id, rating=rating)
            session.add(r)
        session.commit()
        print "The ratings have been added"


def main(session):
    # You'll call each of the load_* functions with the session as an argument
    # load_users(session)
    # load_movies(session)
    # load_ratings(session)
    pass

if __name__ == "__main__":
    s= model.connect()
    main(s)
