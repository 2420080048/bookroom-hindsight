from flask import (
    Blueprint, render_template, session,
    redirect, url_for, flash, current_app,
)

from app import db
from app.forms import BookRequestForm
from app.models.user import User
from app.models.book_request import BookRequest
from app.services.memory_service import save_customer_memory


book_requests = Blueprint("book_requests", __name__)


@book_requests.route("/book-requests", methods=["GET", "POST"])
def request_page():
    customer_id = session.get("customer_id")

    if not customer_id or not db.session.get(User, customer_id):
        return redirect(url_for("auth.login"))

    form = BookRequestForm()

    if form.validate_on_submit():
        text = form.request_text.data.strip()

        if len(text) < 5:
            form.request_text.errors.append(
                "Please describe the book you want."
            )
        else:
            saved_request = BookRequest.query.filter_by(
                customer_id=customer_id,
                request_text=text,
                status="open",
            ).first()

            if not saved_request:
                saved_request = BookRequest(
                    customer_id=customer_id,
                    request_text=text,
                )
                db.session.add(saved_request)
                db.session.commit()

            if saved_request.memory_synced:
                flash("This request is already saved.")
            else:
                try:
                    save_customer_memory(
                        customer_id=customer_id,
                        text=(
                            "The customer submitted this book request: "
                            + text
                        ),
                        event_id=f"book-request-{saved_request.id}",
                    )

                    saved_request.memory_synced = True
                    db.session.commit()
                    flash("Your request was saved and remembered.")

                except Exception as error:
                    db.session.rollback()
                    current_app.logger.warning(
                        "Request memory sync failed: %s",
                        type(error).__name__,
                    )
                    flash(
                        "Your request is saved in the shop database, "
                        "but Hindsight sync failed. Submit the same "
                        "request again to retry without creating a duplicate."
                    )

            return redirect(url_for("book_requests.request_page"))

    requests = (
        BookRequest.query
        .filter_by(customer_id=customer_id)
        .order_by(BookRequest.created_at.desc())
        .all()
    )

    return render_template(
        "book_requests.html",
        form=form,
        requests=requests,
    )