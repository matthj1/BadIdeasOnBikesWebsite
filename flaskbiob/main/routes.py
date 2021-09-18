from flask import Blueprint, flash
from flask import render_template, request
from flask.helpers import url_for
from werkzeug.utils import redirect
from flaskbiob.models import Posts
from flaskbiob.main.forms import ContactForm
from flaskbiob.main.utils import send_contact_message
from smtplib import SMTPAuthenticationError

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


@main.route("/links")
def linksPage():
    return render_template("Links.html")


@main.route("/contact", methods=["GET", "POST"])
def contactPage():
    form = ContactForm()
    if form.validate_on_submit():
        try:
            send_contact_message(form.name.data, form.email.data, form.message.data)
            flash("Your message has been sent!", "success")
            return redirect(url_for("main.homePage"))
        except Exception as E:
            print(E)
            flash("There was a problem sending your message, please try again")
            return redirect(url_for("main.homePage"))
    return render_template("Contact.html", form=form)
