from flask import Flask, render_template, abort, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "bella": generate_password_hash("hello"),
    "alex": generate_password_hash("bye")
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username

@app.route("/")
def splash():
    title = "I Live In Russia"
    text = "Geography Quizzes for everybody who wants to learn more about Russia"
    return render_template('splash.html', title=title, text=text, user = '')

@app.route("/login")
def login():
    title = "Login"
    text = "Here will be form to login"
    return render_template('login.html', title=title, text=text, user = '')


@app.route("/signup")
def signup():
    title = "Sign up"
    text = "Please fill in this form to create an account"
    return render_template('signup.html', title=title, text=text, user = '')


@app.route("/home")
@auth.login_required
def home():
    title = "Games"
    #text = "Here will be catalogue of available quizzes"
    return render_template('games.html', title=title, user = auth.username())


@app.route("/about")
def about():
    title = "About"
    text = "Here will be information about the project"
    return render_template('about.html', title=title, text=text, user = auth.username())


@app.route("/contact")
def contact():
    title = "Contact us"
    text = "Do you have any questions? ideas? notes? We'd love to hear your feedback!"
    return render_template('feedback.html', title=title, text=text, user = auth.username())

@app.route("/profile")
@auth.login_required
def profile():
    title = "Profile"
    text = "Here will be profile information"
    return render_template('profile.html', title=title, text=text, user = auth.username())


@app.route("/logout")
def logout():
    return redirect(url_for('splash'),  code=401)



@app.route("/hellouser")
@auth.login_required
def index():
    return "Hello, {}!".format(auth.username())