from app import create_app, db
from app.models.book import Book

app = create_app()

books_data = [
    ("It Ends With Us", "Colleen Hoover", 149, "Romance"),
    ("Ugly Love", "Colleen Hoover", 149, "Romance"),
    ("The Seven Husbands of Evelyn Hugo", "Taylor Jenkins Reid", 200, "Fiction"),
    ("The Seven Moons of Maali Almeida", "Shehan Karunatilaka", 200, "Fiction"),

    ("Maybe Someday", "Colleen Hoover", 149, "Romance"),
    ("Maybe Not", "Colleen Hoover", 149, "Romance"),
    ("Maybe Now", "Colleen Hoover", 149, "Romance"),

    ("Slammed", "Colleen Hoover", 149, "Romance"),
    ("Point of Retreat", "Colleen Hoover", 149, "Romance"),
    ("This Girl", "Colleen Hoover", 149, "Romance"),

    ("Hopeless", "Colleen Hoover", 149, "Romance"),
    ("Losing Hope", "Colleen Hoover", 149, "Romance"),
    ("Finding Cinderella", "Colleen Hoover", 149, "Romance"),
    ("Finding Perfect", "Colleen Hoover", 149, "Romance"),

    ("All Your Perfects", "Colleen Hoover", 149, "Romance"),
    ("November 9", "Colleen Hoover", 149, "Romance"),

    ("The Fine Print", "Lauren Asher", 200, "Romance"),
    ("Terms and Conditions", "Lauren Asher", 200, "Romance"),
    ("Final Offer", "Lauren Asher", 200, "Romance"),

    ("Throttled", "Lauren Asher", 200, "Romance"),
    ("Collided", "Lauren Asher", 200, "Romance"),
    ("Wrecked", "Lauren Asher", 200, "Romance"),
    ("Redeemed", "Lauren Asher", 200, "Romance"),

    ("Twisted Love", "Ana Huang", 200, "Romance"),
    ("Twisted Games", "Ana Huang", 200, "Romance"),
    ("Twisted Hate", "Ana Huang", 200, "Romance"),
    ("Twisted Lies", "Ana Huang", 200, "Romance"),

    ("King of Wrath", "Ana Huang", 200, "Romance"),
    ("King of Pride", "Ana Huang", 200, "Romance"),

    ("Icebreaker", "Hannah Grace", 200, "Romance"),
    ("The Spanish Love Deception", "Elena Armas", 200, "Romance"),

    ("Heart Bones", "Colleen Hoover", 149, "Romance"),
    ("Reminders of Him", "Colleen Hoover", 149, "Romance"),
    ("Layla", "Colleen Hoover", 149, "Thriller"),
    ("Regretting You", "Colleen Hoover", 149, "Romance"),
    ("Confess", "Colleen Hoover", 149, "Romance"),
    ("Without Merit", "Colleen Hoover", 149, "Fiction"),
    ("Verity", "Colleen Hoover", 200, "Thriller"),
    ("Too Late", "Colleen Hoover", 149, "Thriller"),
    ("Never Never", "Colleen Hoover & Tarryn Fisher", 149, "Romance"),
]


with app.app_context():

    if Book.query.count() > 0:
        print(f"Database already contains {Book.query.count()} books.")
        print("No duplicate books were added.")

    else:

        for title, author, price, genre in books_data:

            book = Book(
                title=title,
                author=author,
                price=price,
                original=499,
                genre=genre,
                stock=1,
                condition="Very Good"
            )

            db.session.add(book)

        db.session.commit()

        print(f"SUCCESS! Added {Book.query.count()} books to the database.")