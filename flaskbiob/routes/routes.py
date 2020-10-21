from flask import render_template, flash, redirect, url_for, request, abort, Blueprint, jsonify, make_response
from flaskbiob.routes.forms import RouteForm
from flaskbiob import db
from flaskbiob.models import Routes
from flask_login import current_user, login_required

routes = Blueprint("routes", __name__)


@routes.route("/route/<post_id>", methods=["GET", "POST"])
@login_required
def newroutePage(post_id):
    form = RouteForm()
    if form.validate_on_submit():
        route = Routes(title=form.title.data, region=form.region.data, starting_location=form.starting_location.data,
                       starting_coordinates=form.starting_coordinates.data, length=form.length.data,
                       ascent=form.ascent.data, description=form.description.data, link=form.link.data,
                       scenery=form.scenery.data, brutality=form.scenery.data, quietness=form.quietness.data,
                       author=current_user, post=post_id)
        db.session.add(route)
        db.session.commit()
        flash("Route created!", "success")
        return redirect(url_for("main.homePage"))
    return render_template("Create_Route.html", title="New Route", form=form)


@routes.route("/routes")
def routesPage():
    my_routes = Routes.query.all()
    for route in my_routes:
        print(route.title)
    return render_template("Routes.html", my_routes=my_routes)
