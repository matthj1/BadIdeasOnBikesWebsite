from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    post_type = SelectField("Post_Type", choices=["Route", "Review", "Other"])
    title = StringField("Title", validators=[DataRequired()])
    leader = TextAreaField("Leader", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[])
    post_image = FileField("Image for this post", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    submit = SubmitField("Post")