from flask import render_template, flash, redirect, url_for, request, abort, Blueprint, jsonify, make_response
from flaskbiob.posts.forms import PostForm
from flaskbiob import db
from flaskbiob.models import Posts, Routes, Reviews
from flask_login import current_user, login_required
from flaskbiob.image_utils import save_post_picture, delete_picture
import urllib.parse

posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def newpostPage():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(post_type=form.post_type.data, title=form.title.data, leader=form.leader.data, content=form.content.data, author=current_user)
        if form.post_image.data:
            picture_file = save_post_picture(form.post_image.data)
            post.post_image = picture_file
        db.session.add(post)
        db.session.commit()
        flash("Post created!", "success")
        return redirect(url_for("main.homePage"))
    return render_template("Create_Post.html", title="New Post", form=form)


@posts.route("/post/<post_id>", methods=["GET", "POST"])
def postPage(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.post_type == "Route":
        route = None
        encoded_title = None
        try:
            route = Routes.query.filter_by(post=post_id).first()
            encoded_title = urllib.parse.quote(route.title)
        except:
            print("No route found")
        return render_template("Post_Route.html", title=post.title, post=post, route=route,
                               encoded_title=encoded_title)
    else:
        review = None
        try:
            review = Reviews.query.filter_by(post=post_id).first()
        except:
            print("No review found")
        return render_template("Post_Review.html", title=post.title, post=post, review=review)


@posts.route("/post/<post_id>/update", methods=["GET", "POST"])
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
        return redirect(url_for("posts.postPage", post_id=post_id))
    elif request.method == "GET":
        form.title.data = post.title
        form.leader.data = post.leader
        form.content.data = post.content
    return render_template("Edit_Post.html", title="Edit Post", form=form)


@posts.route("/post/<post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    if post.post_type == "Route":
        try:
            route = Routes.query.filter_by(post=post_id).first()
            db.session.delete(route)
        except:
            print("No route")
    if post.post_image:
        delete_picture(post.post_image)
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted!", "success")
    return redirect(url_for("main.homePage"))


@posts.route("/imageuploader", methods=["POST"])
def imageuploader():
    file = request.files.get('file')
    if file:
        filename = save_post_picture(file)
        return jsonify({"location": filename})
    output = make_response(404)
    output.headers['Error'] = 'Image failed to upload'
    return output
