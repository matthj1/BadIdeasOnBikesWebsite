from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField, SelectMultipleField, HiddenField, validators
from wtforms.validators import DataRequired


class RouteForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    region = SelectField("Region", choices=["South East", "London", "North West", "East of England", "West Midlands",
                                            "South West", "Yorkshire and Humber", "East Midlands", "North East"])
    starting_location = StringField("Starting Location", validators=[DataRequired()])
    starting_coordinates = StringField("Starting Coordinates", validators=[DataRequired()])
    length = IntegerField("Ride length in km", validators=[DataRequired()])
    ascent = IntegerField("Ride height gain in meters", validators=[DataRequired()])
    description = TextAreaField("Short description of ride", validators=[DataRequired()])
    link = StringField("RWGPS ID", validators=[DataRequired()])
    scenery = SelectField("Rate the scenery out of 5", choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    brutality = SelectField("Rate the brutality out of 5", choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    quietness = SelectField("Rate how quiet the route is out of 5", choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    submit = SubmitField("Submit route")


class RouteFilterForm(FlaskForm):
    # filter by
    region = SelectMultipleField("Region", choices=[("South East", "South East"), ("London", "London"),
                                                    ("North West", "North West"), ("East of England", "East of England"),
                                                    ("West Midlands", "West Midlands"), ("South West", "South West"),
                                                    ("Yorkshire and Humber", "Yorkshire and Humber"),
                                                    ("East Midlands", "East Midlands"), ("North East", "North East")],
                                 validators=[validators.Optional()])
    length_min = HiddenField("Minimum ride length", validators=[validators.Optional()])
    length_max = HiddenField("Maximum ride length", validators=[validators.Optional()])
    ascent_min = HiddenField("Minimum ride ascent", validators=[validators.Optional()])
    ascent_max = HiddenField("Maximum ride ascent", validators=[validators.Optional()])
    scenery_min = HiddenField("Minimum scenery rating", validators=[validators.Optional()])
    scenery_max = HiddenField("Maximum scenery rating", validators=[validators.Optional()])
    brutality_min = HiddenField("Minimum brutality rating", validators=[validators.Optional()])
    brutality_max = HiddenField("Maximum brutality rating", validators=[validators.Optional()])
    quietness_min = HiddenField("Minimum quietness rating", validators=[validators.Optional()])
    quietness_max = HiddenField("Maximum quietness rating", validators=[validators.Optional()])
    #sort by
    sort_by = SelectMultipleField("Sort by:", choices=[("Length ascending", "Length ascending"),
                                                       ("Length descending", "Length descending"),
                                                       ("Ascent ascending", "Ascent ascending"),
                                                       ("Ascent descending", "Ascent descending"),
                                                       ("Scenery ascending", "Scenery ascending"),
                                                       ("Scenery descending", "Scenery descending"),
                                                       ("Brutality ascending", "Brutality ascending"),
                                                       ("Brutality descending", "Brutality descending"),
                                                       ("Quietness ascending", "Quietness ascending"),
                                                       ("Quietness descending", "Quietness descending")],
                                  validators=[validators.Optional()])
    submit = SubmitField("Filter")
