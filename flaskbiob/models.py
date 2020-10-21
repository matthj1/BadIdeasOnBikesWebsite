from flaskbiob import db, login_manager
from flask import current_app
from datetime import datetime
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.png")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Posts", backref="author", lazy=True)
    routes = db.relationship("Routes", backref="author", lazy=True)
    reviews = db.relationship("Reviews", backref="author", lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config["SECRET_KEY"])
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return Users.query.get(user_id)

    def __repr__(self):
        return f"User({self.username},{self.email},{self.image_file})"


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_type = db.Column(db.String(7), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    leader = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    post_image = db.Column(db.String(100), nullable=False, default="default_post.jpg")
    user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    routes = db.relationship("Routes", backref="post_route", lazy=True)
    reviews = db.relationship("Reviews", backref="post_review", lazy=True)

    def __repr__(self):
        return f"Post({self.title},{self.date})"


class Routes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    starting_location = db.Column(db.String(100), nullable=False)
    starting_coordinates = db.Column(db.String(100), nullable=False)
    length = db.Column(db.Integer, nullable=False)
    ascent = db.Column(db.Integer, nullable=False)
    scenery = db.Column(db.Integer, nullable=False)
    brutality = db.Column(db.Integer, nullable=False)
    quietness = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(100), nullable=False)
    post = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=True)
    user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)


class Reviews(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    post = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=True)
    user = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
