from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, IntegerField
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
    link = StringField("Link to RWGPS", validators=[DataRequired()])
    scenery = SelectField("Rate the scenery out of 5", choices=[1, 2, 3, 4, 5])
    brutality = SelectField("Rate the brutality out of 5", choices=[1, 2, 3, 4, 5])
    quietness = SelectField("Rate how quiet the route is out of 5", choices=[1, 2, 3, 4, 5])
    submit = SubmitField("Submit route")
