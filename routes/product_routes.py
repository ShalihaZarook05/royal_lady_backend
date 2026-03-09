from flask import Blueprint, jsonify
from database.db import get_db_connection

product_bp = Blueprint("product_bp", __name__)

# GET ALL PRODUCTS
@product_bp.route("/", methods=["GET"])
def get_products():
    conn = get_db_connection()
    cursor = conn.cursor()

    products = cursor.execute("SELECT * FROM product").fetchall()

    result = []
    for p in products:
        result.append({
            "id": p["id"],
            "name": p["name"],
            "price": p["price"],
            "size": p["size"],
            "brand": p["brand"],
            "description": p["description"],
            "image_url": p["image_url"]
        })

    conn.close()
    return jsonify({"status": "success", "products": result})


# GET SINGLE PRODUCT
@product_bp.route("/<int:product_id>", methods=["GET"])
def get_product(product_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    product = cursor.execute(
        "SELECT * FROM product WHERE id=?",
        (product_id,)
    ).fetchone()

    conn.close()

    if product:
        return jsonify({
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "size": product["size"],
            "brand": product["brand"],
            "description": product["description"],
            "image_url": product["image_url"]
        })

    return jsonify({"error": "Product not found"}), 404
