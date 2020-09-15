from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "2d738b34e9964b74410fd0f284a51bad"

posts = ({
    "author": "Joe Matthews",
    "title": "Kent Climbs",
    "content": "This is a blog post about bike climbs in kent",
    "date": "14/09/2020"
},
    {
    "author": "Joe Matthews",
    "title": "Rutland Circuit",
    "content": "This is a blog post about a bike ride in rutland",
    "date": "13/09/2020"

})

@app.route("/")
@app.route("/home")
def homePage():
    return render_template("Home.html", posts=posts)


@app.route("/about")
def aboutPage():
    return render_template("About.html")


@app.route("/register")
def registerPage():
    form = RegistrationForm()
    return render_template("Register.html")


@app.route("/login")
def loginPage():
    form = LoginForm()
    return render_template("Login.html")



if __name__ == "__main__":
    app.run(debug=True)