import os
from flask import Flask, render_template, request, redirect
from models import db, Supplier, Product, Order

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, "inventory.db")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + database_path
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    print("Database tables created successfully")


@app.route("/")
def dashboard():
    total_products = Product.query.count()
    total_suppliers = Supplier.query.count()
    total_orders = Order.query.count()

    products = Product.query.all()

    if products:
        avg_price = round(sum(product.price for product in products) / len(products), 2)
    else:
        avg_price = 0

    return render_template(
        "dashboard.html",
        total_products=total_products,
        total_suppliers=total_suppliers,
        total_orders=total_orders,
        avg_price=avg_price
    )


@app.route("/suppliers", methods=["GET", "POST"])
def suppliers():
    message = ""

    if request.method == "POST":
        supplier_name = request.form["supplier_name"]
        contact_email = request.form["contact_email"]
        phone_number = request.form["phone_number"]

        existing_supplier = Supplier.query.filter_by(
            contact_email=contact_email
        ).first()

        if existing_supplier:
            message = "Email already exists. Please use a different email."
        else:
            new_supplier = Supplier(
                supplier_name=supplier_name,
                contact_email=contact_email,
                phone_number=phone_number
            )

            db.session.add(new_supplier)
            db.session.commit()
            return redirect("/suppliers")

    suppliers_list = Supplier.query.all()

    return render_template(
        "suppliers.html",
        suppliers=suppliers_list,
        message=message
    )


@app.route("/products", methods=["GET", "POST"])
def products():
    message = ""

    if request.method == "POST":
        product_name = request.form["product_name"]
        category = request.form["category"]
        price = float(request.form["price"])
        quantity = int(request.form["quantity"])
        supplier_id = int(request.form["supplier_id"])

        new_product = Product(
            product_name=product_name,
            category=category,
            price=price,
            quantity=quantity,
            supplier_id=supplier_id
        )

        db.session.add(new_product)
        db.session.commit()
        return redirect("/products")

    products_list = Product.query.all()
    suppliers_list = Supplier.query.all()

    return render_template(
        "products.html",
        products=products_list,
        suppliers=suppliers_list,
        message=message
    )


@app.route("/orders", methods=["GET", "POST"])
def orders():
    message = ""

    if request.method == "POST":
        product_id = int(request.form["product_id"])
        order_quantity = int(request.form["order_quantity"])
        order_date = request.form["order_date"]

        product = Product.query.get(product_id)

        if order_quantity <= 0:
            message = "Order quantity must be greater than zero."
        elif order_quantity > product.quantity:
            message = "Not enough stock available."
        else:
            new_order = Order(
                product_id=product_id,
                order_quantity=order_quantity,
                order_date=order_date
            )

            product.quantity = product.quantity - order_quantity

            db.session.add(new_order)
            db.session.commit()
            return redirect("/orders")

    orders_list = Order.query.all()
    products_list = Product.query.all()

    return render_template(
        "orders.html",
        orders=orders_list,
        products=products_list,
        message=message
    )


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)