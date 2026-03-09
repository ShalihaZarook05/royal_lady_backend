from flask import Blueprint, jsonify
from database.db import get_db_connection

admin_bp = Blueprint("admin_bp", __name__)

# =========================================================
# GET ALL ORDERS (ADMIN)
# =========================================================
@admin_bp.route("/orders", methods=["GET"])
def get_all_orders():

    conn = get_db_connection()
    cursor = conn.cursor()

    orders = cursor.execute("""
        SELECT 
            o.id,
            u.email,
            u.name,
            o.total_price,
            o.order_date
        FROM orders o
        JOIN user u ON u.id = o.user_id
        ORDER BY o.id DESC
    """).fetchall()

    result = []

    for order in orders:
        items = cursor.execute("""
            SELECT p.name, oi.quantity
            FROM order_items oi
            JOIN product p ON p.id = oi.product_id
            WHERE oi.order_id = ?
        """, (order["id"],)).fetchall()

        result.append({
            "id": order["id"],
            "customer": order["name"],
            "email": order["email"],
            "total": order["total_price"],
            "date": order["order_date"],
            "items": [
                {"name": i["name"], "qty": i["quantity"]}
                for i in items
            ]
        })

    conn.close()

    return jsonify({
        "status": "success",
        "orders": result
    })


# =========================================================
# GET ALL USERS (ADMIN)
# =========================================================
@admin_bp.route("/users", methods=["GET"])
def get_all_users():

    conn = get_db_connection()
    cursor = conn.cursor()

    users = cursor.execute("""
        SELECT id, name, email
        FROM user
        ORDER BY id DESC
    """).fetchall()

    result = [
        {
            "id": u["id"],
            "name": u["name"],
            "email": u["email"]
        }
        for u in users
    ]

    conn.close()

    return jsonify({
        "status": "success",
        "users": result
    })


# =========================================================
# DELETE USER
# =========================================================
@admin_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM user WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    if not user:
        conn.close()
        return jsonify({
            "status": "error",
            "message": "User not found"
        }), 404

    cursor.execute("DELETE FROM user WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "User deleted successfully"
    })


# =========================================================
# GET ALL PRODUCTS (ADMIN)
# =========================================================
@admin_bp.route("/products", methods=["GET"])
def get_all_products():

    conn = get_db_connection()
    cursor = conn.cursor()

    products = cursor.execute("""
        SELECT id, name, price
        FROM product
        ORDER BY id DESC
    """).fetchall()

    result = [
        {
            "id": p["id"],
            "name": p["name"],
            "price": p["price"]
        }
        for p in products
    ]

    conn.close()

    return jsonify({
        "status": "success",
        "products": result
    })


# =========================================================
# DELETE PRODUCT
# =========================================================
@admin_bp.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM product WHERE id = ?", (product_id,))
    product = cursor.fetchone()

    if not product:
        conn.close()
        return jsonify({
            "status": "error",
            "message": "Product not found"
        }), 404

    cursor.execute("DELETE FROM product WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Product deleted successfully"
    })


# =========================================================
# CREATE DUMMY USERS
# =========================================================
@admin_bp.route("/create-test-users", methods=["GET"])
def create_test_users():

    conn = get_db_connection()
    cursor = conn.cursor()

    dummy_users = [
        ("Shaliha", "shaliha@gmail.com", "123456"),
        ("Shabeeha", "shabeeha@gmail.com", "123456"),
        ("Kamil", "kamil@gmail.com", "123456"),
        ("Sharuha", "sharuha@gmail.com", "123456"),
        ("Yahya", "yahya@gmail.com", "123456"),
        ("Shiyama", "shiyama@gmail.com", "123456"),
    ]

    for name, email, password in dummy_users:
        cursor.execute("""
            INSERT INTO user (name, email, password)
            VALUES (?, ?, ?)
        """, (name, email, password))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Dummy users created successfully"
    })


# =========================================================
# CREATE DUMMY PRODUCTS (WITHOUT STOCK)
# =========================================================
@admin_bp.route("/create-test-products", methods=["GET"])
def create_test_products():

    conn = get_db_connection()
    cursor = conn.cursor()

    dummy_products = [
        ("Lipstick", 1200),
        ("Foundation", 2500),
        ("Eyeliner", 800),
        ("Face Powder", 1500),
        ("Perfume", 3500),
    ]

    for name, price in dummy_products:
        cursor.execute("""
            INSERT INTO product (name, price)
            VALUES (?, ?)
        """, (name, price))

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Dummy products created successfully"
    })