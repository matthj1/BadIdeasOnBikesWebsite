from flaskbiob import db, bcrypt, create_app
from flaskbiob.models import Users
from email_validator import validate_email, EmailNotValidError
import os

if __name__=="__main__":
    app = create_app()

    validuser = False
    validpassword = False
    validemail = False
    validatepin = False

    with app.app_context():
        while not validatepin:
            pin = input("Please enter security pin: ")
            if pin == os.environ["ADMIN_PIN"]:
                validatepin = True
            else:
                print("Security pin incorrect. Please try again.")
        while not validuser:
            username = input("Please enter username: ")
            if Users.query.filter_by(username=username).first():
                print("Username already exist, please try another username")
            elif len(username) < 4:
                print("Username must be longer than 3 characters")
            else:
                validuser = True
        while not validpassword:
            password = input("Please enter password: ")
            password_confirm = input("Please enter your password again to confirm: ")
            if password != password_confirm:
                print("Your passwords do not match, please try again: ")
            elif len(password) < 6:
                print("Your password must be longer than 5 characters")
            else:
                validpassword = True

        while not validemail:
            email = input("Please enter an email address: ")
            try:
                valid = validate_email(email)
                email = valid.email
            except EmailNotValidError as e:
                print(str(e))
            if Users.query.filter_by(email=email).first():
                print("User with this email already exists, please reset your password online")
            else:
                validemail = True

        print(f"I'm going to commit {username} and {email} to the database")

        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        user = Users(username=username, email=email.lower(), password=hashed_password)
        db.session.add(user)
        db.session.commit()

        print(Users.query.all())