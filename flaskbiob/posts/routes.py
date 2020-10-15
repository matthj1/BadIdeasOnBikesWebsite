from flask import Blueprint
from flask import render_template, flash, redirect, url_for, request, abort
from flaskbiob.posts.forms import PostForm
from flaskbiob import db
from flaskbiob.models import Posts
from flask_login import current_user, login_required
from flaskbiob.image_utils import save_post_picture

posts = Blueprint("posts", __name__)


@posts.route("/post/new", methods=["GET", "POST"])
@login_required
def newpostPage():
    form = PostForm()
    if form.validate_on_submit():
        post = Posts(title=form.title.data, leader=form.leader.data, content=form.content.data, author=current_user)
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
    return render_template("Post.html", title=post.title, post=post)


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
    db.session.delete(post)
    db.session.commit()
    flash("Post deleted!", "success")
    return redirect(url_for("main.homePage"))


