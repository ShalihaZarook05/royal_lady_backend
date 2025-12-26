from flask import Flask, jsonify
from flask_cors import CORS
from database.models import db
from routes.product_routes import product_routes
from routes.recommend_routes import recommend_routes

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///royal.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ✅ REGISTER ROUTES
app.register_blueprint(product_routes)
app.register_blueprint(recommend_routes)

@app.route("/")
def home():
    return jsonify({"message": "Royal Lady Flask Backend is Running!"})

if __name__ == "__main__":
    app.run(debug=True)