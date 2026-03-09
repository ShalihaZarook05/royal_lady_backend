from flask import Flask, jsonify
from flask_cors import CORS
import socket

# DATABASE
from database.db import initialize_db

# ROUTES
from routes.auth_routes import auth_bp
from routes.order_routes import order_bp
from routes.product_routes import product_bp
from routes.recommend_routes import recommend_bp
from routes.admin_routes import admin_bp   # ⭐ ADMIN IMPORT ADDED


# --------------------------------------------------
# CREATE APP
# --------------------------------------------------
app = Flask(__name__)

# Allow Flutter / Mobile / Emulator
CORS(
    app,
    supports_credentials=True,
    resources={r"/api/*": {"origins": "*"}}
)

# --------------------------------------------------
# INITIALIZE DATABASE
# --------------------------------------------------
initialize_db()


# --------------------------------------------------
# REGISTER BLUEPRINT ROUTES
# --------------------------------------------------
app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(order_bp, url_prefix="/api/orders")
app.register_blueprint(product_bp, url_prefix="/api/products")
app.register_blueprint(recommend_bp, url_prefix="/api/recommend")
app.register_blueprint(admin_bp, url_prefix="/api/admin")   # ⭐ ADMIN ROUTES REGISTERED


# --------------------------------------------------
# BASIC ROUTES
# --------------------------------------------------
@app.route("/")
def home():
    return jsonify({
        "status": "success",
        "message": "Royal Lady Backend Running 🚀",
        "base_api": "/api/*"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "success",
        "server": "running"
    })


# --------------------------------------------------
# GET NETWORK IP FOR MOBILE TESTING
# --------------------------------------------------
def get_network_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


# --------------------------------------------------
# RUN SERVER
# --------------------------------------------------
if __name__ == "__main__":
    network_ip = get_network_ip()

    print("\n==============================")
    print("🚀 Royal Lady Backend Started")
    print(f"🖥 Local Access : http://127.0.0.1:5000")
    print(f"📱 Flutter Use  : http://{network_ip}:5000")
    print("👉 Emulator Use : http://10.0.2.2:5000")
    print("==============================\n")

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True,
        use_reloader=False
    )
