from flask import Blueprint, jsonify, request
from database.models import db, Product

product_routes = Blueprint("products", __name__)

# Get all products
@product_routes.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([p.to_dict() for p in products])


# Add a new product
@product_routes.route("/products", methods=["POST"])
def add_product():
    data = request.json
    new_product = Product(
        name=data['name'],
        price=data['price'],
        size=data['size'],
        brand=data['brand'],
        description=data['description'],
        image_url=data['image_url']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added successfully!"})
