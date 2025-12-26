import pickle
from flask import Blueprint, request, jsonify
from sklearn.metrics.pairwise import cosine_similarity

recommend_routes = Blueprint("recommend_routes", __name__)

# --------- Load AI Model Files ----------
with open("model/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

with open("model/product_vectors.pkl", "rb") as f:
    product_vectors = pickle.load(f)

with open("model/product_data.pkl", "rb") as f:
    product_data = pickle.load(f)

@recommend_routes.route("/recommend", methods=["POST"])
def recommend_product():
    data = request.get_json()
    query = data.get("description", "")

    if not query:
        return jsonify({"error": "Description is required"}), 400

    # Vectorize input
    input_vec = vectorizer.transform([query])

    # ✅ CORRECT similarity calculation
    similarity_scores = cosine_similarity(input_vec, product_vectors)[0]

    top_indices = similarity_scores.argsort()[-5:][::-1]

    results = []
    for idx in top_indices:
        results.append({
            "ProductName": product_data[idx]["ProductName"],
            "Brand": product_data[idx]["ProductBrand"],
            "Color": product_data[idx]["PrimaryColor"],
            "Price": product_data[idx]["Price (INR)"],
            "Description": product_data[idx]["Description"]
        })

    return jsonify({"recommendations": results})
