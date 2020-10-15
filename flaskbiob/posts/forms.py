from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    leader = TextAreaField("Leader", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[])
    post_image = FileField("Image for this post", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    submit = SubmitField("Post")