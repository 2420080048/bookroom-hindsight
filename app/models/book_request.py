from datetime import datetime, timezone

from app import db


class BookRequest(db.Model):
    __tablename__ = "book_requests"

    id = db.Column(db.Integer, primary_key=True)

    customer_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    request_text = db.Column(
        db.Text,
        nullable=False,
    )

    status = db.Column(
        db.String(20),
        default="open",
        nullable=False,
    )

    memory_synced = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    customer = db.relationship("User")