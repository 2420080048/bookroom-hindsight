from flask import Blueprint, render_template
from app.models.book import Book


main = Blueprint("main", __name__)


series_bundles = [
    {
        "name": "Twisted Series",
        "author": "Ana Huang",
        "price": 799,
        "theme": "pink",
        "books": [
            {"title": "Twisted Love", "price": 200},
            {"title": "Twisted Games", "price": 200},
            {"title": "Twisted Hate", "price": 200},
            {"title": "Twisted Lies", "price": 200},
        ]
    },

    {
        "name": "Dreamland Billionaires",
        "author": "Lauren Asher",
        "price": 799,
        "theme": "purple",
        "books": [
            {"title": "The Fine Print", "price": 200},
            {"title": "Terms and Conditions", "price": 200},
            {"title": "Final Offer", "price": 200},
        ]
    },

    {
        "name": "Dirty Air Series",
        "author": "Lauren Asher",
        "price": 799,
        "theme": "orange",
        "books": [
            {"title": "Throttled", "price": 200},
            {"title": "Collided", "price": 200},
            {"title": "Wrecked", "price": 200},
            {"title": "Redeemed", "price": 200},
        ]
    },

    {
        "name": "Slammed Trilogy",
        "author": "Colleen Hoover",
        "price": 799,
        "theme": "rose",
        "books": [
            {"title": "Slammed", "price": 149},
            {"title": "Point of Retreat", "price": 149},
            {"title": "This Girl", "price": 149},
        ]
    },

    {
        "name": "Maybe Someday Series",
        "author": "Colleen Hoover",
        "price": 799,
        "theme": "blue",
        "books": [
            {"title": "Maybe Someday", "price": 149},
            {"title": "Maybe Not", "price": 149},
            {"title": "Maybe Now", "price": 149},
        ]
    },
]


@main.route("/")
def home():

    books = Book.query.order_by(Book.id.asc()).all()

    return render_template(
        "index.html",
        books=books,
        series_bundles=series_bundles
    )