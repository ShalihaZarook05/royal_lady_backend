from flask import Blueprint, request, jsonify
import os
import pickle
import pandas as pd
import random
from sklearn.metrics.pairwise import cosine_similarity
from threading import Lock

recommend_bp = Blueprint("recommend_bp", __name__)

# ============================================================
# GLOBAL MODEL STATE
# ============================================================
AI_READY = False
MODEL_LOADING = False
model_lock = Lock()

vectorizer = None
product_vectors = None
products_df = None


# ============================================================
# LOAD MODEL (SAFE + THREAD PROTECTED)
# ============================================================
def load_model():
    global AI_READY, MODEL_LOADING, vectorizer, product_vectors, products_df

    if AI_READY or MODEL_LOADING:
        return

    with model_lock:
        if AI_READY:
            return

        MODEL_LOADING = True
        print("🔄 Loading AI recommendation model...")

        try:
            BASE_DIR = os.path.dirname(os.path.dirname(__file__))
            MODEL_DIR = os.path.join(BASE_DIR, "model")

            vectorizer_path = os.path.join(MODEL_DIR, "vectorizer.pkl")
            vectors_path = os.path.join(MODEL_DIR, "product_vectors.pkl")
            products_path = os.path.join(MODEL_DIR, "products.csv")

            if not os.path.exists(vectorizer_path):
                print("❌ vectorizer.pkl missing")
                return

            if not os.path.exists(vectors_path):
                print("❌ product_vectors.pkl missing")
                return

            if not os.path.exists(products_path):
                print("❌ products.csv missing")
                return

            with open(vectorizer_path, "rb") as f:
                vectorizer = pickle.load(f)

            with open(vectors_path, "rb") as f:
                product_vectors = pickle.load(f)

            products_df = pd.read_csv(products_path)

            AI_READY = True
            print("✅ AI MODEL LOADED SUCCESSFULLY")

        except Exception as e:
            print("❌ AI LOAD FAILED:", str(e))
            AI_READY = False

        finally:
            MODEL_LOADING = False


# ============================================================
# HEALTH CHECK
# ============================================================
@recommend_bp.route("/health", methods=["GET"])
def health():
    load_model()
    return jsonify({"status": "success", "ai_ready": AI_READY})


# ============================================================
# HELPER → FORMAT PRODUCT
# ============================================================
def format_product(product):
    return {
        "ProductName": str(product.get("ProductName", product.get("name", "Item"))),
        "Price": float(product.get("Price", product.get("price", 0)))
    }


# ============================================================
# RECOMMENDATION API
# POST /api/recommend/
# ============================================================
@recommend_bp.route("/", methods=["POST"])
def recommend():

    load_model()

    # -------- MODEL NOT READY --------
    if not AI_READY:
        print("⚠ AI not ready → fallback random")
        sample = products_df.sample(min(5, len(products_df)))
        return jsonify({
            "status": "success",
            "recommendations": [format_product(p) for _, p in sample.iterrows()]
        })

    try:
        data = request.get_json(silent=True) or {}
        description = str(data.get("description", "")).strip()

        # -------- EMPTY DESCRIPTION --------
        if description == "":
            print("⚠ Empty description → random products")
            sample = products_df.sample(min(5, len(products_df)))
            return jsonify({
                "status": "success",
                "recommendations": [format_product(p) for _, p in sample.iterrows()]
            })

        # -------- AI SIMILARITY --------
        user_vector = vectorizer.transform([description])
        similarity = cosine_similarity(user_vector, product_vectors)[0]

        top_indexes = similarity.argsort()[-10:][::-1]

        strong_matches = []
        weak_matches = []

        for idx in top_indexes:
            product = products_df.iloc[idx]

            if similarity[idx] > 0.15:
                strong_matches.append(format_product(product))
            else:
                weak_matches.append(format_product(product))

        # -------- PRIORITY RETURN --------
        if len(strong_matches) >= 3:
            print("✅ Strong AI matches found")
            return jsonify({"status": "success", "recommendations": strong_matches[:5]})

        if len(strong_matches) > 0:
            print("⚠ Weak AI matches → mixed fallback")
            mixed = strong_matches + weak_matches[:5-len(strong_matches)]
            return jsonify({"status": "success", "recommendations": mixed})

        # -------- FULL FALLBACK --------
        print("⚠ No similarity → random fallback")
        sample = products_df.sample(min(5, len(products_df)))
        return jsonify({
            "status": "success",
            "recommendations": [format_product(p) for _, p in sample.iterrows()]
        })

    except Exception as e:
        print("❌ RECOMMEND ERROR:", str(e))

        # FINAL SAFETY NET
        sample = products_df.sample(min(5, len(products_df)))
        return jsonify({
            "status": "success",
            "recommendations": [format_product(p) for _, p in sample.iterrows()]
        })
