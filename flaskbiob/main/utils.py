from flask import url_for
from flaskbiob import mail
from flask_mail import Message
import re


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


def send_contact_message(name, email, message):
    banned_words = ["seo", "jones", "eric", "software", "connections", "marketing"]
    for word in banned_words:
        if word in message.lower():
            print("Spam detected...")
            return
    msg = Message("Bad Ideas on Bikes", sender="Joe Matthews", recipients=["joematthewsphotography@gmail.com"])
    msg.body = f"New message from {name}, {email}:\n {message}"
    mail.send(msg)
