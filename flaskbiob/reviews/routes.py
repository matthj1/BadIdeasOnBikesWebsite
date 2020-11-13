from flask import render_template, flash, redirect, url_for, request, abort, Blueprint, jsonify, make_response
from flaskbiob.reviews.forms import ReviewForm
from flaskbiob import db
from flaskbiob.models import Reviews, Posts
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


@reviews.route("/reviews/<review_id>/update", methods=["GET", "POST"])
@login_required
def updatereviewPage(review_id):
    review = Reviews.query.get_or_404(review_id)
    if review.author != current_user:
        abort(403)
    form = ReviewForm()
    if form.validate_on_submit():
        review.title = form.title.data
        review.category = form.category.data
        review.manufacturer = form.manufacturer.data
        review.product_name = form.product_name.data
        review.rrp = form.RRP.data
        review.rating = form.rating.data
        db.session.commit()
        flash("Post updated!", "success")
        return redirect(url_for("posts.postPage", post_id=review.post))
    elif request.method == "GET":
        form.title.data = review.title
        form.category.data = review.category
        form.manufacturer.data = review.manufacturer
        form.product_name.data = review.product_name
        form.RRP.data = review.rrp
        form.rating.data = review.rating
    return render_template("Edit_Review.html", title="Edit Review", form=form)


@reviews.route("/reviews")
def reviewPage():
    page = request.args.get("page", 1, type=int)
    reviews = db.session.query(Posts).filter(Posts.post_type == "Review").order_by(Posts.date.desc()).paginate(page=page, per_page=10)
    return render_template("Reviews.html", reviews=reviews)


@reviews.route("/reviews/filtered/<review_type>", methods=["GET", "POST"])
def reviewtypePage(review_type):
    reviews = db.session.query(Posts).join(Posts.reviews).filter(Reviews.category == review_type).all()
    return render_template("Reviews.html", reviews=reviews)
