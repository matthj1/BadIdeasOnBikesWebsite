import secrets
import os
from PIL import Image
from flask import render_template, flash, redirect, url_for, request, abort
from flaskbiob.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskbiob import app, db, bcrypt
from flaskbiob.models import Users, Posts
from flask_login import login_user, logout_user, current_user, login_required
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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    image = Image.open(form_picture)

    max_dimension = 125

    size_x, size_y = image.size

    if size_x > size_y:
        scale = size_y / max_dimension
    else:
        scale = size_x / max_dimension

    new_dimensions = (size_x // scale, size_y // scale)
    image.thumbnail(new_dimensions)
    new = image.crop(((new_dimensions[0] - max_dimension) // 2, 0,
                      max_dimension + (new_dimensions[0] - max_dimension) // 2, max_dimension))
    new.save(picture_path)
    return picture_fn


def save_post_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/post_pics', picture_fn)

    image = Image.open(form_picture)

    max_dimension = 1600

    size_x, size_y = image.size

    if size_x > size_y:
        scale = size_x / max_dimension
    else:
        scale = size_y / max_dimension

    new_dimensions = (size_x // scale, size_y // scale)
    image.thumbnail(new_dimensions)
    image.save(picture_path)
    return picture_fn


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