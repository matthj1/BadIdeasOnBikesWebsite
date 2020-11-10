from flask import render_template, flash, redirect, url_for, request, abort, Blueprint, jsonify, make_response
from flaskbiob.reviews.forms import ReviewForm
from flaskbiob import db
from flaskbiob.models import Reviews
from flask_login import current_user, login_required

reviews = Blueprint("reviews", __name__)


@reviews.route("/reviews/<post_id>", methods=["GET", "POST"])
@login_required
def newreviewPage(post_id):
    form = ReviewForm()
    if form.validate_on_submit():
        review = Reviews(title=form.title.data, category=form.category.data, manufacturer=form.manufacturer.data,
                         product_name=form.product_name.data, rrp=form.RRP.data, rating=form.rating.data, post=post_id,
                         author=current_user)
        db.session.add(review)
        db.session.commit()
        flash("Review created!", "success")
        return redirect(url_for("main.homePage"))
    return render_template("Create_Review.html", title="New Route", form=form)
