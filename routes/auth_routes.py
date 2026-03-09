from flask import Blueprint, request, jsonify
from database.db import get_db_connection
import bcrypt

auth_bp = Blueprint("auth_bp", __name__)


# ================= REGISTER =================
@auth_bp.route("/register", methods=["POST"])
def register():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON body"}), 400

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"status": "error", "message": "Missing fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    # check existing
    existing = cursor.execute(
        "SELECT * FROM user WHERE email=?",
        (email,)
    ).fetchone()

    if existing:
        conn.close()
        return jsonify({"status": "error", "message": "User already exists"}), 400

    # hash password
    password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    role = "user"

    cursor.execute(
        "INSERT INTO user (name, email, password_hash, role) VALUES (?, ?, ?, ?)",
        (name, email, password_hash, role)
    )

    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "status": "success",
        "user": {
            "id": user_id,
            "name": name,
            "email": email,
            "role": role
        }
    }), 201


# ================= LOGIN =================
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"status": "error", "message": "Invalid JSON body"}), 400

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"status": "error", "message": "Missing credentials"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    user = cursor.execute(
        "SELECT * FROM user WHERE email=?",
        (email,)
    ).fetchone()

    conn.close()

    if not user:
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    if not bcrypt.checkpw(password.encode(), user["password_hash"].encode()):
        return jsonify({"status": "error", "message": "Invalid credentials"}), 401

    return jsonify({
        "status": "success",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    })
