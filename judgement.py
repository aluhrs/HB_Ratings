from flask import Flask, render_template, redirect, request
import model

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def process_login():
    username = request.form.get("username")
    password = request.form.get("password")
    
    
    return render_template("directory.html")

@app.route("/register")
def register():
    pass

@app.route("/users")
def users():
    user_list = model.session.query(model.User).limit(5).all()
    print user_list
    return render_template("user_list.html", users=user_list)

if __name__ == "__main__":
    app.run(debug = True)