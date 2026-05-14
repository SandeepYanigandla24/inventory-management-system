-- database_setup.sql

-- 1. Create the suppliers table
CREATE TABLE suppliers (
    supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
    supplier_name TEXT NOT NULL,
    contact_email TEXT NOT NULL UNIQUE,
    phone_number TEXT
);

-- 2. Create the products table with a foreign key to suppliers
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL CHECK(price >= 0),
    quantity INTEGER NOT NULL CHECK(quantity >= 0),
    supplier_id INTEGER,
    FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id)
);

-- 3. Create the orders table with a foreign key to products
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER,
    order_quantity INTEGER NOT NULL CHECK(order_quantity > 0),
    order_date TEXT NOT NULL,
    FOREIGN KEY (product_id)
        REFERENCES products(product_id)
);
