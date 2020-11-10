from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, FloatField
from wtforms.validators import DataRequired


class ReviewForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    category = SelectField("Category", choices=["Bike - full build",
                                                "Bike - frame and fork",
                                                "Components - drivetrain",
                                                "Components - wheels",
                                                "Components - tyres",
                                                "Components - brakes",
                                                "Components - saddles",
                                                "Components - Pedals",
                                                "Components - bars, stems and posts",
                                                "Components - other",
                                                "Accessories - GPS & Computers",
                                                "Accessories - Power Meters",
                                                "Accessories - Lights",
                                                "Accessories - Trainers",
                                                "Accessories - Other",
                                                "Clothing - Tops",
                                                "Clothing - Bottoms",
                                                "Clothing - Base",
                                                "Clothing - Jackets",
                                                "Clothing - Shoes",
                                                "Clothing - Helmets",
                                                "Clothing - Glasses",
                                                "Clothing - Other",
                                                "Workshop - Tools",
                                                "Workshop - Cleaning",
                                                "Workshop - Lubricant",
                                                "Workshop - Other",
                                                "Other - Other"
                                                ])

    rating = SelectField("Rating", choices=[1, 2, 3, 4, 5])
    manufacturer = StringField("Manufacturer", validators=[DataRequired()])
    product_name = StringField("Product Name", validators=[DataRequired()])
    RRP = FloatField("RRP", validators=[DataRequired()])
    submit = SubmitField("Post")