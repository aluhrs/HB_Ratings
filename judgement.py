from flask import Flask, render_template, redirect, request, flash, url_for, session

import model

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'


@app.route("/")
def index():
    if session.get("username"):
        return redirect(url_for("directory", username=[session['username']]))
    else:
        return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")
    authentication = model.authenticate(username, password)

    if authentication:
        flash("User authenticated")
        session['username'] = username
    else:
        flash("Password incorrect. Would you like to register an account?")
    
    return redirect(url_for("index"))

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def registered():
    username = request.form.get("username")
    password = request.form.get("password")
    password_verify = request.form.get("password_verify")

    if password == password_verify:
        authentication = model.authenticate(username, password)
        if authentication:
            flash("You are already in the database. Please login.")
            return redirect(url_for("index"))
        else:
            model.create_user(username, password)
            flash("You have successfully created an account! Please login!")
            return redirect(url_for("index"))
    else:
        flash("Your passwords do not match. Please try again.")

    return redirect(url_for("registered"))    

@app.route("/close")
def close():
    session.clear()

    return redirect(url_for("index"))


@app.route("/users")
def users():
    user_list = model.session.query(model.User).limit(5).all()
    return render_template("user_list.html", users=user_list)

@app.route("/ratings/<userid>")
def ratings(userid):
    # Check that the userid is valid
    isValidUser = model.session.query(model.User).filter_by(id = userid).one()
    # query using the userid adn return their ratings
    if isValidUser:
        ratings = isValidUser.ratings
        # user_ratings = model.session.query(model.Rating).filter_by(user_id = userid).all()
        return render_template("ratings.html", user_ratings=ratings, user_id = userid)
    else:
        # Put a placeholder for flash messages in user_list.html
        flash("The user does not exist")
        return redirect(url_for("users"))
 
@app.route("/ratemovie/<movieid>")
def rateMovie(movieid):
    movie_name = model.session.query(model.Movie).filter_by(id = movieid).one()

    # if the person is logged in:
    try:
        if session['username']:
            user = model.session.query(model.User).filter_by(email = session['username']).one()
            user_id = user.id
            current_rating = model.session.query(model.Rating).filter_by(user_id = user.id, movie_id = movieid).all()
            print current_rating
            return render_template("ratemovie.html", movie_rating=current_rating, movie=movie_name, userid = user_id)
    except KeyError:
        flash("You must be logged in to rate a movie. Please log in or create an account.")
        return redirect(url_for("index"))

@app.route("/ratemovie/<movieid>", methods=["POST"])
def rate_movie_DB(movieid):
    user = model.session.query(model.User).filter_by(email = session['username']).one()
    user_id = user.id
    current_rating = model.session.query(model.Rating).filter_by(user_id = user.id, movie_id = movieid).all()
    print current_rating
    rating = request.form.get("create_rating")
    if current_rating == []:
        create_rating = model.Rating(user_id=user.id, movie_id=movieid, rating=rating)
        print create_rating
        model.session.add(create_rating)
        model.session.commit()
        return "User %s has rated movie id %s a %s" % (user_id, movieid, rating)
    else:
        print rating
        current_rating[0].rating = rating
        #session.add(update_rating)
    # commit the user to the database
        model.session.commit()
        return "User %s rated movie id %s a %s. Your new rating is %s" % (user_id, movieid, current_rating[0].rating, rating)

@app.route("/movies")
def movies():
    movies = model.session.query(model.Movie).limit(5).all()
    return render_template("movies.html", movies=movies)

@app.route("/movie/<movieid>")
def view_movie(movieid):
    movie = model.session.query(model.Movie).get(movieid)
    ratings = movie.ratings
    rating_nums = []
    user_rating = None
    user = model.session.query(model.User).filter_by(email = session['username']).one()
    user_id = user.id
    for r in ratings:
        if r.user_id == user.id:
            user_rating = r
        rating_nums.append(r.rating)
    avg_rating = float(sum(rating_nums))/len(rating_nums)

    u = model.session.query(model.User).get(user_id)
    prediction = None
    if not user_rating:
        prediction = u.predict_rating(movie)

    return render_template("movie.html", movie=movie, average=avg_rating, user_rating=user_rating, prediction=prediction)

    



@app.route("/directory/<username>")
def directory(username):
    return render_template("directory.html")

if __name__ == "__main__":
    app.run(debug=True)