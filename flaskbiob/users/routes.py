from flask import Blueprint

from flask import render_template, flash, redirect, url_for, request
from flaskbiob.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flaskbiob import db, bcrypt
from flaskbiob.models import Users, Posts
from flask_login import login_user, logout_user, current_user, login_required
from flaskbiob.image_utils import save_picture
from flaskbiob.main.utils import send_reset_email


users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def registerPage():
    if current_user.is_authenticated:
        return redirect(url_for("main.homePage"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = Users(username=form.username.data, email=form.email.data.lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account created!", "success")
        return redirect(url_for("users.loginPage"))
    else:
        return render_template("Register.html", title="Register", form=form)


@users.route("/login", methods=["GET", "POST"])
def loginPage():
    if current_user.is_authenticated:
        return redirect(url_for("main.homePage"))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("main.homePage"))
        else:
            flash("Login unsuccessful", "danger")
    return render_template("Login.html", title="Login", form=form)


@users.route("/logout")
def logoutPage():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for("main.homePage"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def accountPage():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data.lower()
        db.session.commit()
        flash("Account Updated!", "success")
        return redirect(url_for("users.accountPage"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template("Account.html", title="Account", image_file=image_file, form=form)


@users.route("/reset_password", methods=["GET", "POST"])
def resetrequestPage():
    if current_user.is_authenticated:
        return redirect(url_for("main.homePage"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("Email sent, please check your inbox", "info")
        return redirect(url_for("users.loginPage"))
    return render_template("Reset_Request.html", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def resetPage(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.homePage"))
    user = Users.verify_reset_token(token)
    if not user:
        flash("Invalid or expired reset request", "warning")
        return redirect(url_for("users.resetrequestPage"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash("Password Updated", "success")
        return redirect(url_for("users.loginPage"))
    return render_template("Reset_Token.html", form=form)


@users.route("/user/<string:username>")
def userpostPage(username):
    page = request.args.get("page", 1, type=int)
    user = Users.query.filter_by(username=username).first_or_404()
    posts = Posts.query.filter_by(author=user)\
        .order_by(Posts.date.desc())\
        .paginate(page=page, per_page=5)
    return render_template("User_Posts.html", posts=posts, user=user)