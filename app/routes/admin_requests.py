from flask import Blueprint, render_template, current_app
from flask_wtf import FlaskForm
from wtforms import SubmitField

from app.models.book_request import BookRequest
from app.routes.admin import admin_required
from app.services.request_matching_service import (
    check_request_stock,
    draft_customer_message,
)


admin_requests = Blueprint(
    "admin_requests",
    __name__,
    url_prefix="/admin",
)


class StockCheckForm(FlaskForm):
    submit = SubmitField("Check matching stock")
    draft = SubmitField("Draft customer message")


def render_requests(
    form,
    selected_id=None,
    result=None,
    draft=None,
    error=None,
):
    requests = (
        BookRequest.query
        .order_by(BookRequest.created_at.desc())
        .all()
    )

    return render_template(
        "admin/book_requests.html",
        requests=requests,
        form=form,
        selected_id=selected_id,
        result=result,
        draft=draft,
        error=error,
    )


@admin_requests.route("/book-requests")
@admin_required
def dashboard():
    return render_requests(StockCheckForm())


@admin_requests.route(
    "/book-requests/<int:request_id>/check",
    methods=["POST"],
)
@admin_required
def check_stock(request_id):
    form = StockCheckForm()
    book_request = BookRequest.query.get_or_404(request_id)

    if not form.validate_on_submit():
        return render_requests(
            form,
            selected_id=request_id,
            error="Please reopen Customer Book Requests and try again.",
        ), 400

    if not book_request.memory_synced:
        return render_requests(
            form,
            selected_id=request_id,
            error="This request needs to sync with Hindsight first.",
        )

    try:
        if form.draft.data:
            draft = draft_customer_message(book_request)

            if not draft:
                raise ValueError("Empty message draft")

            return render_requests(
                form,
                selected_id=request_id,
                draft=draft,
            )

        result = check_request_stock(book_request)

        if not result:
            raise ValueError("Empty stock assessment")

        return render_requests(
            form,
            selected_id=request_id,
            result=result,
        )

    except Exception as error:
        current_app.logger.warning(
            "Admin request action failed: %s",
            type(error).__name__,
        )

        return render_requests(
            form,
            selected_id=request_id,
            error="The request could not finish. Please try again.",
        )