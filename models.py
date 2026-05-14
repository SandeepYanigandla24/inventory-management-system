from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Supplier(db.Model):
    __tablename__ = 'suppliers'

    supplier_id = db.Column(db.Integer, primary_key=True)
    supplier_name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20))

    products = db.relationship('Product', backref='supplier', lazy=True)


class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

    supplier_id = db.Column(
        db.Integer,
        db.ForeignKey('suppliers.supplier_id'),
        nullable=False
    )


class Order(db.Model):
    __tablename__ = 'orders'

    order_id = db.Column(db.Integer, primary_key=True)

    product_id = db.Column(
        db.Integer,
        db.ForeignKey('products.product_id'),
        nullable=False
    )

    order_quantity = db.Column(db.Integer, nullable=False)
    order_date = db.Column(db.String(50), nullable=False)