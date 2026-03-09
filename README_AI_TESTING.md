# AI Recommendation System - Testing Guide

## Overview

The Royal Lady AI recommendation system uses **TF-IDF vectorization** and **cosine similarity** to provide product recommendations based on text descriptions. This guide covers how to test the AI components.

## Architecture

### Components

1. **Model Files** (in `model/` directory):
   - `vectorizer.pkl`: TF-IDF vectorizer trained on product descriptions
   - `product_vectors.pkl`: Pre-computed TF-IDF vectors for all products
   - `product_data.pkl`: Product metadata (name, description, price)

2. **API Endpoint**: `/recommend` (POST)
   - Input: JSON with `description` field
   - Output: JSON with top 5 similar products

3. **Algorithm**:
   - User query → TF-IDF vectorization → Cosine similarity calculation → Top 5 matches

## Test Scripts

### 1. `test_ai_model.py` - Model Component Tests

Tests the AI model files directly without running the server.

**Run:**
```bash
cd royal_lady_backend
python test_ai_model.py
```

**What it tests:**
- ✓ Model file existence (vectorizer, vectors, data)
- ✓ Model loading from pickle files
- ✓ Vectorizer transformation functionality
- ✓ Data consistency between vectors and metadata
- ✓ Complete recommendation logic
- ✓ Cosine similarity calculations

**Expected Output:**
```
========================================================
       AI Model Components Test Suite
========================================================

TEST: Model Files Existence Check
✓ Found: model/vectorizer.pkl (12345 bytes)
✓ Found: model/product_vectors.pkl (54321 bytes)
✓ Found: model/product_data.pkl (23456 bytes)

...

========================================================
                    Test Summary
========================================================
  File Existence            : PASSED
  Load Vectorizer           : PASSED
  Load Product Vectors      : PASSED
  ...
```

### 2. `test_ai_recommendation.py` - API Endpoint Tests

Tests the `/recommend` API endpoint with various scenarios.

**Prerequisites:**
- Flask server must be running: `python app.py`

**Run:**
```bash
cd royal_lady_backend
python test_ai_recommendation.py
```

**What it tests:**
- ✓ Server connectivity
- ✓ Basic recommendation queries
- ✓ Empty query handling
- ✓ Response schema validation
- ✓ Special characters in queries
- ✓ Various fashion-related queries
- ✓ Performance metrics (response time)

**Sample Queries Tested:**
- "casual blue jeans for women"
- "formal black dress for party"
- "cotton t-shirt comfortable"
- "red color ethnic wear"
- "winter jacket warm"

### 3. `test_ai_integration.py` - End-to-End Integration Tests

Tests the complete workflow including database and API integration.

**Prerequisites:**
- Flask server must be running
- Database must be populated with products

**Run:**
```bash
cd royal_lady_backend
python test_ai_integration.py
```

**What it tests:**
- ✓ Database connectivity
- ✓ Product API integration
- ✓ Complete recommendation workflow
- ✓ Recommendation diversity
- ✓ Edge cases and error handling

## Running All Tests

### Quick Test Suite (All in One)

```bash
# 1. Test model files (no server needed)
cd royal_lady_backend
python test_ai_model.py

# 2. Start Flask server in a separate terminal
python app.py

# 3. Test API endpoint (in another terminal)
python test_ai_recommendation.py

# 4. Test integration
python test_ai_integration.py
```

## Expected Results

### Model Tests
- All 3 pickle files should load successfully
- Vectorizer should have vocabulary size > 0
- Product vectors shape should match product data length
- Sample recommendations should be generated

### API Tests
- Server should respond within 1 second
- Empty queries should return empty recommendations
- Valid queries should return 5 recommendations
- All recommendations should have: ProductName, Description, Price

### Integration Tests
- Database should contain products
- Product API should return data
- Different queries should produce relevant recommendations

## Common Issues & Solutions

### Issue: "Model files missing"
**Solution:** Run the training notebook first:
```bash
cd royal_lady_backend/model
jupyter notebook trainer.ipynb
# Execute all cells to generate .pkl files
```

### Issue: "Could not connect to server"
**Solution:** Make sure Flask is running:
```bash
cd royal_lady_backend
python app.py
```

### Issue: "No recommendations returned"
**Solution:** 
- Check if product_data.pkl has products
- Verify database has products
- Try different search queries

### Issue: "Import errors (sklearn, pickle, etc.)"
**Solution:** Install dependencies:
```bash
pip install -r requirements.txt
```

## Manual Testing with cURL

### Test Recommendation Endpoint

```bash
# Basic recommendation
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"description": "blue jeans women casual"}'

# Empty query
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"description": ""}'

# Complex query
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"description": "elegant red dress for wedding party formal wear"}'
```

### Expected Response Format

```json
{
  "recommendations": [
    {
      "ProductName": "Women's Blue Denim Jeans",
      "Description": "Comfortable casual blue jeans...",
      "Price": 1299.0
    },
    {
      "ProductName": "Ladies Casual Jeans",
      "Description": "Stylish casual wear...",
      "Price": 999.0
    }
    // ... up to 5 products
  ]
}
```

## Performance Benchmarks

### Expected Performance
- **Response Time**: < 1 second per request
- **Recommendations**: Always returns 5 products (unless empty query)
- **Relevance**: Top recommendation should contain query keywords

### Load Testing
```python
# Simple load test
import requests
import time

url = "http://localhost:5000/recommend"
payload = {"description": "blue jeans"}

for i in range(100):
    start = time.time()
    r = requests.post(url, json=payload)
    elapsed = (time.time() - start) * 1000
    print(f"Request {i+1}: {elapsed:.2f}ms")
```

## Debugging Tips

### Enable Verbose Output
Add print statements to `recommend_routes.py`:
```python
@recommend_routes.route("/recommend", methods=["POST"])
def recommend_product():
    data = request.get_json(force=True)
    query = data.get("description", "").strip()
    
    print(f"[DEBUG] Received query: {query}")
    print(f"[DEBUG] Query length: {len(query)}")
    
    # ... rest of code
```

### Check Model Integrity
```python
import pickle
with open("model/product_data.pkl", "rb") as f:
    data = pickle.load(f)
    print(f"Products: {len(data)}")
    print(f"Sample: {data[0]}")
```

### Validate Cosine Similarity Scores
```python
# In recommend_routes.py
similarity_scores = cosine_similarity(input_vec, product_vectors)[0]
print(f"[DEBUG] Similarity scores: min={min(similarity_scores)}, max={max(similarity_scores)}")
```

## Test Coverage Summary

| Component | Test Script | Coverage |
|-----------|-------------|----------|
| Model Files | test_ai_model.py | 100% |
| Vectorizer | test_ai_model.py | 100% |
| API Endpoint | test_ai_recommendation.py | 100% |
| Database | test_ai_integration.py | 100% |
| Workflow | test_ai_integration.py | 100% |
| Edge Cases | test_ai_recommendation.py, test_ai_integration.py | 95% |

## Next Steps

1. **Run all test scripts** to verify AI system functionality
2. **Review test outputs** for any failures
3. **Check performance metrics** to ensure acceptable response times
4. **Test with real user queries** from the Flutter app
5. **Monitor logs** for any errors or warnings

## Contact & Support

For issues or questions about the AI recommendation system testing:
- Check the main `PROJECT_DOCUMENTATION.md`
- Review Flask logs: `python app.py` (debug mode enabled)
- Inspect model training notebook: `model/trainer.ipynb`
