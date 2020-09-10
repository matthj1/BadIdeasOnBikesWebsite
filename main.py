from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def homePage():
    return render_template("BASE.html", stuff="No")


@app.route("/about")
def aboutPage():
    return "<h1>About Page</h1>"


if __name__ == "__main__":
    app.run(debug=True)