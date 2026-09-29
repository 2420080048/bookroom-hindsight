from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    Length,
)


class RegisterForm(FlaskForm):
    name = StringField(
        "Your name",
        validators=[DataRequired(), Length(min=2, max=100)],
    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=255)],
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8, max=128)],
    )

    confirm_password = PasswordField(
        "Confirm password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match."),
        ],
    )

    submit = SubmitField("Create account")


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=255)],
    )

    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(max=128)],
    )

    submit = SubmitField("Log in")


class MemoryForm(FlaskForm):
    preference = StringField(
        "Tell us your book preferences",
        validators=[Length(max=1000)],
    )

    save = SubmitField("Remember this")
    recall = SubmitField("Recall my preferences")
    recommend = SubmitField("Recommend books")
class BookRequestForm(FlaskForm):
    request_text = StringField(
        "What book are you looking for?",
        validators=[DataRequired(), Length(min=5, max=1000)],
    )

    submit = SubmitField("Save my book request")