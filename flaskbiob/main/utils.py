from flask import url_for
from flaskbiob import mail
from flask_mail import Message


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password reset request", sender="Joe Matthews", recipients=[user.email])
    msg.body = f'''To reset your password please visit this link:
{url_for("users.resetPage", token=token, _external=True)}
If you did not make this request, please ignore this message.

Thanks,

Bad Ideas on Bikes
'''
    mail.send(msg)