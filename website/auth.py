'''
Date: 2021-10-30 20:04:22
LastEditors: GC
LastEditTime: 2021-11-04 11:48:00
FilePath: \Flask-Project\website\auth.py
'''

from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


# Create a bluprint for our flask application
auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

    # Check for validation
        user = User.query.filter_by(email=email).first()
        if user:
            # We did actually find a user, and we need to check if the password they typed in is equal to the hash that we have stored
            #   in the server.
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")

                login_user(user, remember=True)

                # Redirect the user to the home page
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password! Please try again!", category="error")
        else:
            flash("Email does not exist.", category="error")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
# To make sure we can not log out if we are not logged in
@login_required
def logout():
    logout_user()

    # Redirect to the login page after we logged out the account
    return redirect(url_for("auth.login"))


@auth.route("/sign-up", methods=["POST", "GET"])
def sign_up():
    if request.method == "POST":

        # Get all the information from the form
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Check the validation
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exist!", category="error")

        elif len(email) < 4:
            flash("Email must be greater than 3 charactors.", category="error")
        elif len(first_name) < 2:
            flash("First name must be greater than 1 charactor.", category="error")
        elif password1 != password2:
            flash("Password don\'t match.", category="error")
        elif len(password1) < 7:
            flash("Password must be at lease 7 charactors.", category="error")
        else:
            # Create new user account:
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(
                password1, method='sha256'))

            # Add this account to the database:
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Account created successfully !", category="success")

            # Redirect the user to the home page
            return redirect(url_for("views.home"))
    return render_template("sign_up.html", user=current_user)
