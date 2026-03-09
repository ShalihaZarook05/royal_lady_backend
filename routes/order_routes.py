from flask import Blueprint, request, jsonify
from database.db import get_db_connection

order_bp = Blueprint("order_bp", __name__)

# =========================================================
# PLACE ORDER (ACCEPT /orders AND /orders/)
# =========================================================
@order_bp.route("", methods=["POST"])
@order_bp.route("/", methods=["POST"])
def create_order():
    data = request.get_json(silent=True) or {}

    items = data.get("items", [])
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"status": "error", "message": "User ID required"}), 400

    if not items:
        return jsonify({"status": "error", "message": "No items in order"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    total = 0

    # ---------- CALCULATE TOTAL ----------
    for item in items:
        product = cursor.execute(
            "SELECT price FROM product WHERE id=?",
            (item["product_id"],)
        ).fetchone()

        if not product:
            continue

        total += float(product["price"]) * int(item["quantity"])

    # ---------- CREATE ORDER ----------
    cursor.execute(
        "INSERT INTO orders (user_id, total_price) VALUES (?, ?)",
        (user_id, total)
    )
    order_id = cursor.lastrowid

    # ---------- INSERT ORDER ITEMS ----------
    for item in items:
        cursor.execute(
            "INSERT INTO order_items (order_id, product_id, quantity) VALUES (?, ?, ?)",
            (order_id, item["product_id"], item["quantity"])
        )

    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": "Order created",
        "order_id": order_id
    }), 201


# =========================================================
# GET ORDERS BY USER
# =========================================================
@order_bp.route("/<int:user_id>", methods=["GET"])
def get_orders(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    orders = cursor.execute(
        "SELECT * FROM orders WHERE user_id = ? ORDER BY id DESC",
        (user_id,)
    ).fetchall()

    result = []

    for order in orders:
        items = cursor.execute("""
            SELECT p.name, p.price, oi.quantity
            FROM order_items oi
            JOIN product p ON p.id = oi.product_id
            WHERE oi.order_id = ?
        """, (order["id"],)).fetchall()

        result.append({
            "id": order["id"],
            "date": order["order_date"],
            "total": order["total_price"],
            "items": [dict(item) for item in items]
        })

    conn.close()

    return jsonify({
        "status": "success",
        "orders": result
    })
