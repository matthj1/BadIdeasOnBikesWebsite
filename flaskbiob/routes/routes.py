from flask import render_template, flash, redirect, url_for, request, abort, Blueprint, jsonify, make_response
from flaskbiob.routes.forms import RouteForm, RouteFilterForm
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


@routes.route("/routes/<route_id>/update", methods=["GET", "POST"])
@login_required
def updateroutePage(route_id):
    route = Routes.query.get_or_404(route_id)
    if route.author != current_user:
        abort(403)
    form = RouteForm()
    if form.validate_on_submit():
        route.title = form.title.data
        route.region = form.region.data
        route.starting_location = form.starting_location.data
        route.starting_coordinates = form.starting_coordinates.data
        route.length = form.length.data
        route.ascent = form.ascent.data
        route.description = form.description.data
        route.link = form.link.data
        route.scenery = form.scenery.data
        route.brutality = form.brutality.data
        route.quietness = form.quietness.data
        db.session.commit()
        flash("Post updated!", "success")
        return redirect(url_for("posts.postPage", post_id=route.post))
    elif request.method == "GET":
        form.title.data = route.title
        form.region.data = route.region
        form.starting_location.data = route.starting_location
        form.starting_coordinates.data = route.starting_coordinates
        form.length.data = route.length
        form.ascent.data = route.ascent
        form.description.data = route.description
        form.link.data = route.link
        form.scenery.data = route.scenery
        form.brutality.data = route.brutality
        form.quietness.data = route.quietness
    return render_template("Edit_Route.html", title="Edit Route", form=form)


@routes.route("/routes", methods=["GET", "POST"])
def routesPage():
    form = RouteFilterForm()
    query = Routes.query
    if form.validate_on_submit():
        if form.region.data:
            query = query.filter(Routes.region == form.region.data[0])
        if form.length_min.data:
            query = query.filter(Routes.length >= form.length_min.data)
        if form.length_max.data:
            query = query.filter(Routes.length <= form.length_max.data)
        if form.ascent_min.data:
            query = query.filter(Routes.ascent >= form.ascent_min.data)
        if form.ascent_max.data:
            query = query.filter(Routes.ascent <= form.ascent_max.data)
        if form.scenery_min.data and form.scenery_min.data != "None":
            query = query.filter(Routes.scenery >= form.scenery_min.data)
        if form.scenery_max.data and form.scenery_max.data != "None":
            query = query.filter(Routes.scenery <= form.scenery_max.data)
        if form.brutality_min.data and form.brutality_min.data != "None":
            query = query.filter(Routes.brutality >= form.brutality_min.data)
        if form.brutality_max.data and form.brutality_max.data != "None":
            query = query.filter(Routes.brutality <= form.brutality_max.data)
        if form.quietness_min.data and form.quietness_min.data != "None":
            query = query.filter(Routes.quietness >= form.quietness_min.data)
        if form.quietness_max.data and form.quietness_max.data != "None":
            query = query.filter(Routes.quietness <= form.quietness_max.data)
        if form.sort_by.data:
            if form.sort_by.data[0] == "Length ascending":
                query = query.order_by(Routes.length.asc())
            elif form.sort_by.data[0] == "Length descending":
                query = query.order_by(Routes.length.desc())
            elif form.sort_by.data[0] == "Ascent ascending":
                query = query.order_by(Routes.ascent.asc())
            elif form.sort_by.data[0] == "Ascent descending":
                query = query.order_by(Routes.ascent.desc())
            elif form.sort_by.data[0] == "Scenery ascending":
                query = query.order_by(Routes.scenery.asc())
            elif form.sort_by.data[0] == "Scenery descending":
                query = query.order_by(Routes.scenery.desc())
            elif form.sort_by.data[0] == "Brutality ascending":
                query = query.order_by(Routes.brutality.asc())
            elif form.sort_by.data[0] == "Brutality descending":
                query = query.order_by(Routes.brutality.desc())
            elif form.sort_by.data[0] == "Quietness ascending":
                query = query.order_by(Routes.quietness.asc())
            elif form.sort_by.data[0] == "Quietness descending":
                query = query.order_by(Routes.quietness.desc())
        results = query.all()
        print(results)
        return render_template("Routes.html", my_routes=results, form=form, filtered=True)
    my_routes = Routes.query.all()
    return render_template("Routes.html", my_routes=my_routes, form=form, filtered=False)
