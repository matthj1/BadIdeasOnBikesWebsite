from flask import Flask, render_template, flash, redirect, url_for
from My_Forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "2d738b34e9964b74410fd0f284a51bad"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Posts", backref="Author", lazy=True)

    def __repr__(self):
        return f"User({self.username},{self.email},{self.image_file})"


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return f"Post({self.title},{self.date})"


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


if __name__ == "__main__":
    app.run(debug=True)