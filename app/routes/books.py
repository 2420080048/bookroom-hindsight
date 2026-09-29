from app import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(200),
        nullable=False
    )

    author = db.Column(
        db.String(150),
        nullable=False
    )

    price = db.Column(
        db.Integer,
        nullable=False
    )

    original = db.Column(
        db.Integer,
        default=499
    )

    genre = db.Column(
        db.String(100),
        nullable=False
    )

    stock = db.Column(
        db.Integer,
        default=1
    )

    condition = db.Column(
        db.String(50),
        default="Very Good"
    )

    cover_url = db.Column(
        db.String(500),
        nullable=True
    )

    def __repr__(self):
        return f"<Book {self.title}>"