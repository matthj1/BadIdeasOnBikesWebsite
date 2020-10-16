from flask import Blueprint
from flask import render_template, request
from flaskbiob.models import Posts

main = Blueprint("main", __name__)


@main.route("/")
@main.route("/home")
def homePage():
    page = request.args.get("page", 1, type=int)
    posts = Posts.query.order_by(Posts.date.desc()).paginate(page=page, per_page=5)
    return render_template("Home.html", posts=posts)


@main.route("/about")
def aboutPage():
    return render_template("About.html")

@main.route("/routes")
def routesPage():
    return render_template("Routes.html")