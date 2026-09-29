from flask import (
    Blueprint, render_template, redirect,
    url_for, session,
)
from sqlalchemy.exc import IntegrityError

from app import db
from app.forms import RegisterForm, LoginForm
from app.models.user import User


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    error = None

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        name = form.name.data.strip()

        if len(name) < 2:
            error = "Please enter your name."
        elif User.query.filter_by(email=email).first():
            error = "This email is already registered. Please log in."
        else:
            user = User(name=name, email=email)
            user.set_password(form.password.data)

            db.session.add(user)

            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                error = "This email is already registered."
            else:
                session.clear()
                session["customer_id"] = user.id
                return redirect(url_for("main.home"))

    return render_template(
        "auth/account.html",
        form=form,
        error=error,
        registering=True,
    )


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    error = None

    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(form.password.data):
            session.clear()
            session["customer_id"] = user.id
            return redirect(url_for("main.home"))

        error = "Incorrect email or password."

    return render_template(
        "auth/account.html",
        form=form,
        error=error,
        registering=False,
    )