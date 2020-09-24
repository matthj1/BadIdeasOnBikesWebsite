from flask import render_template, flash, redirect, url_for
from flaskbiob.forms import RegistrationForm, LoginForm
from flaskbiob import app
from flaskbiob.models import Users, Posts

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
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"account created for {form.username.data}", "success")
        return redirect(url_for("homePage"))
    else:
        return render_template("Register.html", title="Register", form=form)


@app.route("/login", methods=["GET", "POST"])
def loginPage():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "admin@test.com" and form.password.data == "password":
            flash(f"login successful for {form.email.data}", "success")
            return redirect(url_for("homePage"))
        else:
            flash("Login unsuccessful", "danger")
    return render_template("Login.html", title="Login", form=form)
