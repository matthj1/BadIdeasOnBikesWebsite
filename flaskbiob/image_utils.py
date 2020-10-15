import os
import secrets
from PIL import Image
from flask import current_app


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    image = Image.open(form_picture)

    max_dimension = 125

    size_x, size_y = image.size

    if size_x > size_y:
        scale = size_y / max_dimension
    else:
        scale = size_x / max_dimension

    new_dimensions = (size_x // scale, size_y // scale)
    image.thumbnail(new_dimensions)
    new = image.crop(((new_dimensions[0] - max_dimension) // 2, 0,
                      max_dimension + (new_dimensions[0] - max_dimension) // 2, max_dimension))
    new.save(picture_path)
    return picture_fn


def save_post_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/post_pics', picture_fn)

    image = Image.open(form_picture)

    max_dimension = 1600

    size_x, size_y = image.size

    if size_x > size_y:
        scale = size_x / max_dimension
    else:
        scale = size_y / max_dimension

    new_dimensions = (size_x // scale, size_y // scale)
    image.thumbnail(new_dimensions)
    image.save(picture_path)
    return picture_fn
