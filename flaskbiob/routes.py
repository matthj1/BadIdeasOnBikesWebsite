import secrets
import os
from PIL import Image
from flask import render_template, flash, redirect, url_for, request
from flaskbiob.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskbiob import app, db, bcrypt
from flaskbiob.models import Users, Posts
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import func

posts = ({
    "author": "Joe Matthews",
    "title": "Kent Climbs",
    "content": "This is a blog post about bike climbs in kent",
    "date": "14/09/2020",
    "image": "static/Chalkpit Lane.jpg"
},
    {
    "author": "Joe Matthews",
    "title": "Rutland Circuit",
    "content": "This is a blog post about a bike ride in rutland",
    "date": "13/09/2020",
    "image": "static/Big.jpg"

})


@app.route("/")
@app.route("/home")
def homePage():
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
