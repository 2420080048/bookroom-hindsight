import json

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for
)

from app import db
from app.models.book import Book
from app.models.order import Order, OrderItem


orders = Blueprint(
    "orders",
    __name__
)


BUNDLE_PRICES = {
    "Twisted Series": 799,
    "Dreamland Billionaires": 799,
    "Dirty Air Series": 799,
    "Slammed Trilogy": 799,
    "Maybe Someday Series": 799
}


@orders.route(
    "/checkout",
    methods=["GET", "POST"]
)
def checkout():

    error = None

    if request.method == "POST":

        customer_name = request.form.get(
            "customer_name",
            ""
        ).strip()

        phone = request.form.get(
            "phone",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip()

        address = request.form.get(
            "address",
            ""
        ).strip()

        city = request.form.get(
            "city",
            ""
        ).strip()

        pincode = request.form.get(
            "pincode",
            ""
        ).strip()

        payment_method = request.form.get(
            "payment_method",
            "Cash on Delivery"
        )

        notes = request.form.get(
            "notes",
            ""
        ).strip()

        cart_data = request.form.get(
            "cart_data",
            "[]"
        )

        try:
            cart = json.loads(cart_data)

        except json.JSONDecodeError:
            cart = []


        if not cart:

            error = "Your cart is empty."

            return render_template(
                "orders/checkout.html",
                error=error
            )


        if not all([
            customer_name,
            phone,
            address,
            city,
            pincode
        ]):

            error = "Please fill all required details."

            return render_template(
                "orders/checkout.html",
                error=error
            )


        validated_items = []

        total = 0


        for item in cart:

            title = str(
                item.get("title", "")
            ).strip()

            if not title:
                continue


            book = Book.query.filter_by(
                title=title
            ).first()


            if book:

                price = book.price
                author = book.author

            elif title in BUNDLE_PRICES:

                price = BUNDLE_PRICES[title]

                author = item.get(
                    "author",
                    "Complete Collection"
                )

            else:

                continue


            validated_items.append({
                "title": title,
                "author": author,
                "price": price
            })

            total += price


        if not validated_items:

            error = "We could not process the books in your cart."

            return render_template(
                "orders/checkout.html",
                error=error
            )


        new_order = Order(
            customer_name=customer_name,
            phone=phone,
            email=email or None,
            address=address,
            city=city,
            pincode=pincode,
            payment_method=payment_method,
            notes=notes or None,
            total_amount=total,
            status="Placed"
        )


        db.session.add(new_order)

        db.session.flush()


        for item in validated_items:

            order_item = OrderItem(
                order_id=new_order.id,
                title=item["title"],
                author=item["author"],
                price=item["price"],
                quantity=1
            )

            db.session.add(order_item)


        db.session.commit()


        return redirect(
            url_for(
                "orders.order_success",
                order_id=new_order.id
            )
        )


    return render_template(
        "orders/checkout.html",
        error=error
    )


@orders.route(
    "/order-success/<int:order_id>"
)
def order_success(order_id):

    order = Order.query.get_or_404(
        order_id
    )

    return render_template(
        "orders/success.html",
        order=order
    )