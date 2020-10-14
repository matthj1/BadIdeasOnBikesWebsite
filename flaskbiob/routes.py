import secrets
import os
from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort
from flaskbiob.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from flaskbiob import app, db, bcrypt, mail
from flaskbiob.models import Users, Posts
from flask_login import login_user, logout_user, current_user, login_required
from flaskbiob.image_utils import save_picture, save_post_picture
from flask_mail import Message
from sqlalchemy import func

@app.route("/")
@app.route("/home")
def homePage():
    page = request.args.get("page", 1, type=int)
    posts = Posts.query.order_by(Posts.date.desc()).paginate(page=page, per_page=5)
    return render_template("Home.html", posts=posts)


@app.route("/about")
def aboutPage():
    return render_template("About.html")


@app.route("/register", methods=["GET", "POST"])
def registerPage():
    if current_user.is_authenticated:
        return redirect(url_for("homePage"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = Users(username=form.username.data, email=form.email.data.lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Account created!", "success")
        return redirect(url_for("loginPage"))
    else:
        return render_template("Register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def loginPage():
    if current_user.is_authenticated:
        return redirect(url_for("homePage"))
    form = LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data.lower()).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("homePage"))
        else:
            flash("Login unsuccessful", "danger")
    return render_template("Login.html", title="Login", form=form)


@app.route("/logout")
def logoutPage():
    logout_user()
    flash("Logged out successfully", "success")
    return redirect(url_for("homePage"))


@app.route("/account", methods=["GET", "POST"])
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
        return redirect(url_for("accountPage"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template("Account.html", title="Account", image_file=image_file, form=form)


@app.route("/post/new", methods=["GET", "POST"])
@login_required
def newpostPage():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data, leader=form.leader.data, content=form.content.data, author=current_user)
        if form.post_image.data:
            picture_file = save_post_picture(form.post_image.data)
            post.post_image = picture_file
        db.session.add(post)
        db.session.commit()
        flash("Post created!", "success")
        return redirect(url_for("homePage"))
    return render_template("Create_Post.html", title="New Post", form=form)


@app.route("/post/<post_id>", methods=["GET", "POST"])
def postPage(post_id):
    post = Posts.query.get_or_404(post_id)
    return render_template("Post.html", title=post.title, post=post)


@app.route("/post/<post_id>/update", methods=["GET", "POST"])
@login_required
def updatepostPage(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        if form.post_image.data:
            picture_file = save_post_picture(form.post_image.data)
            post.post_image = picture_file
        post.title = form.title.data
        post.leader = form.leader.data
        post.content = form.content.data
        db.session.commit()
        flash("Post updated!", "success")
        return redirect(url_for("postPage", post_id=post_id))
    elif request.method == "GET":
        form.title.data = post.title
        form.leader.data = post.leader
        form.content.data = post.content
    return render_template("Edit_Post.html", title="Edit Post", form=form)


@app.route("/post/<post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted!", "success")
    return redirect(url_for("homePage"))


@app.route("/user/<string:username>")
def userpostPage(username):
    page = request.args.get("page", 1, type=int)
    user = Users.query.filter_by(username=username).first_or_404()
    posts = Posts.query.filter_by(author=user)\
        .order_by(Posts.date.desc())\
        .paginate(page=page, per_page=5)
    return render_template("User_Posts.html", posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password reset request", sender="Joe Matthews", recipients=[user.email])
    msg.body = f'''To reset your password please visit this link:
{url_for("resetPage", token=token, _external=True)}
If you did not make this request, please ignore this message.

Thanks,

Bad Ideas on Bikes
'''
    mail.send(msg)


@app.route("/reset_password", methods=["GET", "POST"])
def resetrequestPage():
    if current_user.is_authenticated:
        return redirect(url_for("homePage"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("Email sent, please check your inbox", "info")
        return redirect(url_for("loginPage"))
    return render_template("Reset_Request.html", form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def resetPage(token):
    if current_user.is_authenticated:
        return redirect(url_for("homePage"))
    user = Users.verify_reset_token(token)
    if not user:
        flash("Invalid or expired reset request", "warning")
        return redirect(url_for("resetrequestPage"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash("Password Updated", "success")
        return redirect(url_for("loginPage"))
    return render_template("Reset_Token.html", form=form)
