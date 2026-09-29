from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config


db = SQLAlchemy()


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)


    # Main website
    from app.routes.main import main

    app.register_blueprint(main)
    from app.routes.auth import auth
    app.register_blueprint(auth)
    from app.routes.assistant import assistant
    app.register_blueprint(assistant)
    from app.routes.book_requests import book_requests
    app.register_blueprint(book_requests)
    from app.routes.admin_requests import admin_requests
    app.register_blueprint(admin_requests)


    # Admin dashboard
    from app.routes.admin import admin

    app.register_blueprint(admin)


    # Checkout and orders
    from app.routes.orders import orders

    app.register_blueprint(orders)


    # Database models
    from app.models.book import Book
    from app.models.user import User
    from app.models.book_request import BookRequest

    from app.models.order import (
        Order,
        OrderItem
    )


    with app.app_context():

        db.create_all()


    return app