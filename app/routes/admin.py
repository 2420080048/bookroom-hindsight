import re
from functools import wraps
from urllib.parse import quote
from hmac import compare_digest

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    current_app
)

from app import db
from app.models.book import Book
from app.models.order import Order


admin = Blueprint(
    "admin",
    __name__,
    url_prefix="/admin"
)


# ============================================================
# ADMIN LOGIN PROTECTION
# ============================================================

def admin_required(function):

    @wraps(function)
    def decorated_function(*args, **kwargs):

        if not session.get("admin_logged_in"):

            return redirect(
                url_for("admin.login")
            )

        return function(*args, **kwargs)

    return decorated_function


# ============================================================
# ADMIN LOGIN
# ============================================================

@admin.route(
    "/login",
    methods=["GET", "POST"]
)
def login():

    error = None

    if session.get("admin_logged_in"):

        return redirect(
            url_for("admin.dashboard")
        )

    if request.method == "POST":

        username = request.form.get(
            "username",
            ""
        ).strip()

        password = request.form.get(
            "password",
            ""
        )

        correct_username = str(
            current_app.config.get(
                "ADMIN_USERNAME",
                ""
            )
        )

        correct_password = str(
            current_app.config.get(
                "ADMIN_PASSWORD",
                ""
            )
        )

        username_correct = compare_digest(
            username,
            correct_username
        )

        password_correct = compare_digest(
            password,
            correct_password
        )

        if username_correct and password_correct:

            session.clear()

            session[
                "admin_logged_in"
            ] = True

            return redirect(
                url_for(
                    "admin.dashboard"
                )
            )

        error = (
            "Incorrect username or password."
        )

    return render_template(
        "admin/login.html",
        error=error
    )


# ============================================================
# ADMIN LOGOUT
# ============================================================

@admin.route("/logout")
def logout():

    session.clear()

    return redirect(
        url_for("admin.login")
    )


# ============================================================
# ADMIN DASHBOARD
# ============================================================

@admin.route("/")
@admin_required
def dashboard():

    books = Book.query.order_by(
        Book.id.desc()
    ).all()

    total_books = len(books)

    total_stock = sum(
        book.stock
        for book in books
    )

    total_orders = Order.query.count()

    placed_orders = (
        Order.query
        .filter_by(
            status="Placed"
        )
        .count()
    )

    return render_template(
        "admin/dashboard.html",
        books=books,
        total_books=total_books,
        total_stock=total_stock,
        total_orders=total_orders,
        placed_orders=placed_orders
    )


# ============================================================
# VIEW ALL ORDERS
# ============================================================

@admin.route("/orders")
@admin_required
def orders():

    all_orders = (
        Order.query
        .order_by(
            Order.created_at.desc()
        )
        .all()
    )

    return render_template(
        "admin/orders.html",
        orders=all_orders
    )


# ============================================================
# NORMAL ORDER STATUS UPDATE
# ============================================================

@admin.route(
    "/orders/<int:order_id>/status",
    methods=["POST"]
)
@admin_required
def update_order_status(order_id):

    order = Order.query.get_or_404(
        order_id
    )

    new_status = request.form.get(
        "status"
    )

    allowed_statuses = [
        "Placed",
        "Confirmed",
        "Packed",
        "Shipped",
        "Delivered",
        "Cancelled"
    ]

    if new_status in allowed_statuses:

        order.status = new_status

        db.session.commit()

    return redirect(
        url_for("admin.orders")
    )


# ============================================================
# WHATSAPP HELPERS
# ============================================================

def clean_whatsapp_number(phone):

    # Remove spaces, +, -, brackets, etc.
    digits = re.sub(
        r"\D",
        "",
        str(phone)
    )

    # Indian 10-digit number
    # 9876543210 → 919876543210
    if len(digits) == 10:

        digits = "91" + digits

    # 09876543210 → 919876543210
    elif (
        len(digits) == 11
        and
        digits.startswith("0")
    ):

        digits = (
            "91"
            + digits[1:]
        )

    return digits


def get_order_whatsapp_message(order):

    order_number = (
        f"BR{order.id:04d}"
    )

    customer = (
        order.customer_name
    )

    total = (
        order.total_amount
    )

    # Build book names
    book_names = []

    for item in order.items:

        book_names.append(
            f"• {item.title}"
        )

    books_text = "\n".join(
        book_names
    )

    if order.status == "Placed":

        message = (
            f"Hi {customer}! 📚\n\n"
            f"We received your order "
            f"#{order_number} from "
            f"The Book Room.\n\n"
            f"{books_text}\n\n"
            f"Order Total: ₹{total}\n\n"
            f"We'll update you once "
            f"your order is confirmed. ♡"
        )

    elif order.status == "Confirmed":

        message = (
            f"Hi {customer}! 📚✨\n\n"
            f"Great news! Your order "
            f"#{order_number} has been "
            f"*CONFIRMED*.\n\n"
            f"{books_text}\n\n"
            f"Order Total: ₹{total}\n\n"
            f"We're getting your books "
            f"ready for you. ♡\n\n"
            f"— The Book Room"
        )

    elif order.status == "Packed":

        message = (
            f"Hi {customer}! 📦📚\n\n"
            f"Your order #{order_number} "
            f"has been *PACKED*.\n\n"
            f"Your books are ready and "
            f"waiting for dispatch. ♡\n\n"
            f"— The Book Room"
        )

    elif order.status == "Shipped":

        message = (
            f"Hi {customer}! 🚚📚\n\n"
            f"Your order #{order_number} "
            f"has been *SHIPPED*!\n\n"
            f"Your books are officially "
            f"on their way to you. 💗\n\n"
            f"— The Book Room"
        )

    elif order.status == "Delivered":

        message = (
            f"Hi {customer}! 💗📚\n\n"
            f"Your order #{order_number} "
            f"has been *DELIVERED*.\n\n"
            f"We hope you absolutely love "
            f"your new reads!\n\n"
            f"Thank you for shopping with "
            f"The Book Room. ♡"
        )

    elif order.status == "Cancelled":

        message = (
            f"Hi {customer},\n\n"
            f"Your order #{order_number} "
            f"from The Book Room has been "
            f"*CANCELLED*.\n\n"
            f"If you have any questions, "
            f"please contact us."
        )

    else:

        message = (
            f"Hi {customer}! 📚\n\n"
            f"Your order #{order_number} "
            f"status is now "
            f"*{order.status}*.\n\n"
            f"— The Book Room"
        )

    return message


# ============================================================
# UPDATE STATUS + OPEN WHATSAPP
# ============================================================

@admin.route(
    "/orders/<int:order_id>/status-whatsapp",
    methods=["POST"]
)
@admin_required
def update_order_status_whatsapp(
    order_id
):

    order = Order.query.get_or_404(
        order_id
    )

    new_status = request.form.get(
        "status"
    )

    allowed_statuses = [
        "Placed",
        "Confirmed",
        "Packed",
        "Shipped",
        "Delivered",
        "Cancelled"
    ]

    if new_status in allowed_statuses:

        order.status = new_status

        db.session.commit()

    phone = clean_whatsapp_number(
        order.phone
    )

    message = (
        get_order_whatsapp_message(
            order
        )
    )

    encoded_message = quote(
        message,
        safe=""
    )

    whatsapp_url = (
        f"https://wa.me/"
        f"{phone}"
        f"?text={encoded_message}"
    )

    return redirect(
        whatsapp_url
    )


# ============================================================
# MESSAGE CUSTOMER WITHOUT CHANGING STATUS
# ============================================================

@admin.route(
    "/orders/<int:order_id>/whatsapp"
)
@admin_required
def whatsapp_customer(order_id):

    order = Order.query.get_or_404(
        order_id
    )

    phone = clean_whatsapp_number(
        order.phone
    )

    message = (
        get_order_whatsapp_message(
            order
        )
    )

    encoded_message = quote(
        message,
        safe=""
    )

    whatsapp_url = (
        f"https://wa.me/"
        f"{phone}"
        f"?text={encoded_message}"
    )

    return redirect(
        whatsapp_url
    )


# ============================================================
# ADD BOOK
# ============================================================

@admin.route(
    "/add",
    methods=["GET", "POST"]
)
@admin_required
def add_book():

    if request.method == "POST":

        title = request.form[
            "title"
        ]

        author = request.form[
            "author"
        ]

        price = int(
            request.form["price"]
        )

        genre = request.form[
            "genre"
        ]

        stock = int(
            request.form["stock"]
        )

        condition = request.form.get(
            "condition",
            "Very Good"
        )

        cover_url = request.form.get(
            "cover_url",
            ""
        )

        new_book = Book(
            title=title,
            author=author,
            price=price,
            original=499,
            genre=genre,
            stock=stock,
            condition=condition,
            cover_url=cover_url
        )

        db.session.add(
            new_book
        )

        db.session.commit()

        return redirect(
            url_for(
                "admin.dashboard"
            )
        )

    return render_template(
        "admin/add_book.html"
    )


# ============================================================
# EDIT BOOK
# ============================================================

@admin.route(
    "/edit/<int:book_id>",
    methods=["GET", "POST"]
)
@admin_required
def edit_book(book_id):

    book = Book.query.get_or_404(
        book_id
    )

    if request.method == "POST":

        book.title = request.form[
            "title"
        ]

        book.author = request.form[
            "author"
        ]

        book.price = int(
            request.form["price"]
        )

        book.genre = request.form[
            "genre"
        ]

        book.stock = int(
            request.form["stock"]
        )

        book.condition = request.form[
            "condition"
        ]

        book.cover_url = request.form.get(
            "cover_url",
            ""
        )

        db.session.commit()

        return redirect(
            url_for(
                "admin.dashboard"
            )
        )

    return render_template(
        "admin/edit_book.html",
        book=book
    )


# ============================================================
# DELETE BOOK
# ============================================================

@admin.route(
    "/delete/<int:book_id>",
    methods=["POST"]
)
@admin_required
def delete_book(book_id):

    book = Book.query.get_or_404(
        book_id
    )

    db.session.delete(
        book
    )

    db.session.commit()

    return redirect(
        url_for(
            "admin.dashboard"
        )
    )