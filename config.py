import os
from dotenv import load_dotenv


BASE_DIR = os.path.abspath(
    os.path.dirname(__file__)
)


# Always load the .env file
# from the project folder
load_dotenv(
    os.path.join(
        BASE_DIR,
        ".env"
    )
)


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-secret-key"
    )

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///"
        + os.path.join(
            BASE_DIR,
            "bookstore.db"
        )
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    ADMIN_USERNAME = os.getenv(
        "ADMIN_USERNAME",
        "admin"
    )

    ADMIN_PASSWORD = os.getenv(
        "ADMIN_PASSWORD",
        "change-me"
    )

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"