from uuid import uuid4

from flask import (
    Blueprint,
    render_template,
    session,
    redirect,
    url_for,
    current_app,
)

from app import db
from app.forms import MemoryForm
from app.models.user import User
from app.services.memory_service import (
    save_customer_memory,
    recall_customer_memory,
)
from app.services.recommendation_service import recommend_books


assistant = Blueprint("assistant", __name__)


@assistant.route("/assistant", methods=["GET", "POST"])
def memory_page():
    customer_id = session.get("customer_id")

    if not customer_id or not db.session.get(User, customer_id):
        return redirect(url_for("auth.login"))

    form = MemoryForm()
    message = None
    memories = []
    recommendations = None

    if form.validate_on_submit():
        try:
            if form.save.data:
                text = (form.preference.data or "").strip()

                if not text:
                    message = "Please enter a preference first."
                else:
                    save_customer_memory(
                        customer_id=customer_id,
                        text=text,
                        event_id=str(uuid4()),
                    )
                    message = "Your preference was saved in Hindsight."

            elif form.recall.data:
                memories = recall_customer_memory(
                    customer_id,
                    "What are this customer's book preferences, "
                    "budget, and book condition requirements?",
                )

                if not memories:
                    message = "No preferences found yet."

            elif form.recommend.data:
                recommendations = recommend_books(customer_id)

                if not recommendations:
                    message = "No answer was returned. Please try again."

        except Exception as error:
            current_app.logger.warning(
                "Assistant operation failed: %s",
                type(error).__name__,
            )
            message = (
                "We could not complete this request. "
                "If you have not saved any preferences, save one first. "
                "Otherwise, check your Hindsight connection and credits."
            )

    return render_template(
        "assistant.html",
        form=form,
        message=message,
        memories=memories,
        recommendations=recommendations,
    )