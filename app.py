import flask
from flask import Flask, render_template, abort, redirect, url_for, request
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
#from flask_httpauth import HTTPBasicAuth
from database import create_user, get_user_by_name
from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email
from urllib.parse import urlparse, urljoin
import os


app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


app.secret_key = os.urandom(12).hex()

class User():
    def __init__(self, username):
        self.username = username

    def is_active(self):
        return True
    def is_authenticated(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return self.username
    @classmethod
    def get(cls,username):
        return User(username)


@login_manager.user_loader
def load_user(username):
    return User.get(username)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

class LoginForm(FlaskForm):
    username = StringField('Username', render_kw={'class':'form__input', 'placeholder':'Enter Username'},validators=[DataRequired()])
    password = PasswordField('Password', render_kw={'class':'form__input', 'placeholder':'Enter Password'},validators=[DataRequired()])
    submit = SubmitField('Submit', render_kw={'class':'form__submit'})

class SignUpForm(FlaskForm):
    username = StringField('Username', render_kw={'class':'form__input', 'placeholder':'Enter Username'},validators=[DataRequired()])
    # name = StringField('Name', render_kw={'class':'form__input', 'placeholder':'Enter Name'}, validators=[DataRequired()])
    # age = IntegerField('Age', validators=[DataRequired()])
    # country = StringField('Country', validators=[DataRequired()])
    password = PasswordField('Password', render_kw={'class':'form__input', 'placeholder':'Enter Password'}, validators=[DataRequired()])
    submit = SubmitField('Submit', render_kw={'class':'form__submit'})

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    list = ['Submit', 'CSRF Token']
    form = LoginForm()
    title = "Login"
    post = 'login'
    password = "Forgotten your password?"
    direction = 'signup'
    question = 'Dont have an account?'
    direction_text = 'Sign up'
    if form.validate_on_submit():
        # Login and validate the user.
        # print('username', form.username.data)
        username = form.username.data
        password = form.password.data

        user_b = get_user_by_name(username)

        if user_b and \
            check_password_hash(user_b['Password'], password):

            user = User(username)

        # user should be an instance of your `User` class
            login_user(user)
        
            flask.flash('Logged in successfully.')

            next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
            if not is_safe_url(next):
                return flask.abort(400)

            return flask.redirect(next or flask.url_for('home'))
    return flask.render_template('login.html', form=form, title = title, list = list, post = post, password = password, direction_text = direction_text, question=question, direction = direction )

@app.route("/settings")
@login_required
def settings():
    pass

@app.route('/test')
@login_required
def test():
    return render_template('test.html')


@app.route("/")
def splash():
    title = "I Live In Russia"
    text = "Geography Quizzes for everybody who wants to learn more about Russia"
    return render_template('splash.html', title=title, text=text, user = '')



@app.route("/signup", methods=['GET', 'POST'])
def signup():
    title = "Sign up"
    text = "Please fill in this form to create an account"
    post = 'signup'
    direction = 'login'
    question = 'Already have an account?'
    direction_text = 'Login'
    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        password_hash = generate_password_hash(password)

        
        # name = form.name.data
        # bio = form.bio.data
        # age = form.age.data

        #validate
        #it is not an existing username
        #username/password are not empty
        # put them in a database!
        #create_user(username, password)

        create_user(username, password_hash)

        user = User(username)
        # user should be an instance of your `User` class
        login_user(user)
        
        flask.flash('Logged in successfully.')
        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('home'))
    return render_template('login.html', title=title, text=text, form = form,  post = post, direction_text = direction_text, question=question, direction = direction )


@app.route("/home")
@login_required
def home():
    title = "Games"
    #text = "Here will be catalogue of available quizzes"
    username = current_user.username
    return render_template('games.html', user = username)


@app.route("/about")
def about():
    title = "About"
    text = "Geography quizzes help to lea"
    if current_user.is_authenticated:
        user = current_user.username
    else: user =''
    return render_template('about.html', title=title, text=text)


@app.route("/contact")
def contact():
    title = "Contact us"
    text = "Do you have any questions? ideas? notes? We'd love to hear your feedback!"
    if current_user.is_authenticated:
        user = current_user.username
    else: user =''
    return render_template('feedback.html', title=title, text=text, user = user)

@app.route("/profile")
@login_required
def profile():
    title = "Profile"
    text = "Here will be profile information"
    return render_template('profile.html', title=title, text=text, user = current_user.username)


# @app.route("/logout")
# def logout():
#     return redirect(url_for('splash'),  code=401)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('splash'))


# @app.route("/hellouser")
# @login_required
# def index():
#     return "Hello, {}!".format(auth.username())