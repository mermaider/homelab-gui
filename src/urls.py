# standard imports
from flask_login import login_user, login_required, logout_user, current_user
from flask import render_template, flash, request, redirect, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

# local code imports
from models import *
from forms import LoginForm, PostForm
from app import app

basicAuth = HTTPBasicAuth()


@basicAuth.verify_password
def verify_password(user, password):
    user = User.query.filter_by(username=user.username).first()

    if user and check_password_hash(user.password, password):
        return user

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))
    loginform = LoginForm()
    if loginform.validate_on_submit():
        user = User.query.filter_by(username=loginform.username.data).first()
        if user and check_password_hash(user.password_hash, loginform.password.data):
            login_user(user, remember=loginform.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("dashboard"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", loginform=loginform)


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!  Thanks For Stopping By...")
    return redirect(url_for("login"))


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/posts", methods=["GET","POST"])
@login_required
def posts():
    posts = post_factory.find_posts_by_username(current_user.username)
    return render_template("posts.html", posts=posts)


@app.route("/posts/edit/<post_id>", methods=["GET","POST"])
@login_required
def edit_post(post_id):
    postform = PostForm()
    post = post_factory.get(post_id)
    if postform.validate_on_submit():
        post.title = postform.title.data
        post.content = postform.content.data
        post.insert()

    return render_template("edit-post.html", postform=postform)
