# 🧪 Complete AI Testing Guide - Royal Lady

## 📖 Table of Contents
1. [Quick Start](#quick-start)
2. [Test Scripts Overview](#test-scripts-overview)
3. [Step-by-Step Testing](#step-by-step-testing)
4. [Manual Testing](#manual-testing)
5. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Fastest Way to Test (3 Commands)

```bash
# Terminal 1: Start Flask server
cd royal_lady_backend
python app.py

# Terminal 2: Run quick test
cd royal_lady_backend
python test_ai_quick.py "blue jeans casual"

# Expected: 5 product recommendations
```

---

## 📦 Test Scripts Overview

| Script | Purpose | Server Required | Time |
|--------|---------|----------------|------|
| `test_ai_model.py` | Test model files | ❌ No | 2-3s |
| `test_ai_recommendation.py` | Test API endpoint | ✅ Yes | 5-10s |
| `test_ai_integration.py` | Test full workflow | ✅ Yes | 8-12s |
| `test_ai_quick.py` | Quick single test | ✅ Yes | 1s |
| `run_all_ai_tests.py` | Run all tests | ✅ Yes | 15-25s |

---

## 🎯 Step-by-Step Testing

### Phase 1: Model Validation (No Server Needed)

**Goal**: Verify AI model files are properly generated and functional

```bash
cd royal_lady_backend
python test_ai_model.py
```

**What's Being Tested**:
1. ✅ `vectorizer.pkl` exists and loads
2. ✅ `product_vectors.pkl` exists and loads
3. ✅ `product_data.pkl` exists and loads
4. ✅ Data consistency (vectors count = data count)
5. ✅ Vectorizer can transform text
6. ✅ Cosine similarity works
7. ✅ Complete recommendation logic

**Expected Output**:
```
============================================================
            AI Model Components Test Suite
============================================================

TEST: Model Files Existence Check
✓ Found: model/vectorizer.pkl (12345 bytes)
✓ Found: model/product_vectors.pkl (54321 bytes)
✓ Found: model/product_data.pkl (23456 bytes)

------------------------------------------------------------

TEST: Loading Vectorizer
✓ Vectorizer loaded successfully
ℹ Type: TfidfVectorizer
ℹ Vocabulary size: 500 words

------------------------------------------------------------

... (more tests)

============================================================
                    Test Summary
============================================================
  File Existence            : PASSED
  Load Vectorizer           : PASSED
  Load Product Vectors      : PASSED
  Load Product Data         : PASSED
  Data Consistency          : PASSED
  Vectorizer Transform      : PASSED
  Recommendation Logic      : PASSED

============================================================
✓ ALL TESTS PASSED (7/7)
```

**If Tests Fail**: See [Troubleshooting](#troubleshooting) section

---

### Phase 2: API Endpoint Testing (Server Required)

**Goal**: Verify the `/recommend` endpoint works correctly

**Step 1**: Start Flask Server (Terminal 1)
```bash
cd royal_lady_backend
python app.py
```

You should see:
```
 * Running on http://127.0.0.1:5000
 * Restarting with stat
 * Debugger is active!
```

**Step 2**: Run API Tests (Terminal 2)
```bash
cd royal_lady_backend
python test_ai_recommendation.py
```

**What's Being Tested**:
1. ✅ Server connectivity
2. ✅ Basic recommendations for query
3. ✅ Empty query handling
4. ✅ Response schema validation
5. ✅ Special characters handling
6. ✅ Various fashion queries
7. ✅ Performance benchmarking

**Expected Output**:
```
============================================================
    Royal Lady AI Recommendation System - Test Suite
============================================================

TEST: Server Connection Test
✓ Server is running: {'message': 'Royal Lady Flask Backend is Running!'}

------------------------------------------------------------

TEST: Basic Recommendation Test - Query: 'blue jeans women casual'
✓ Request successful - Status: 200
✓ Found 5 recommendations

  Recommendation 1:
    Product: Women's Blue Denim Jeans
    Price: ₹1299
    Description: Comfortable casual blue jeans...

... (4 more recommendations)

------------------------------------------------------------

... (more tests)

============================================================
                    Test Summary
============================================================
  Server Connection         : PASSED
  Basic Recommendation      : PASSED
  Empty Query               : PASSED
  Response Schema           : PASSED
  Special Characters        : PASSED
  Fashion Queries           : PASSED
  Performance               : PASSED

============================================================
✓ ALL TESTS PASSED (7/7)
```

---

### Phase 3: Integration Testing (Full System)

**Goal**: Test complete workflow with database

**Prerequisites**:
- Flask server running (from Phase 2)
- Database populated with products

**Run**:
```bash
cd royal_lady_backend
python test_ai_integration.py
```

**What's Being Tested**:
1. ✅ Database connectivity
2. ✅ Product API (`/products` endpoint)
3. ✅ Complete recommendation workflow
4. ✅ Recommendation diversity
5. ✅ Edge cases (empty, special chars, etc.)

**Expected Output**:
```
============================================================
        AI Recommendation Integration Test Suite
============================================================

TEST: Database Connectivity Test
✓ Database connected: royal.db
ℹ Total products in database: 50

------------------------------------------------------------

TEST: Product API Test
✓ Product API working - Retrieved 50 products

------------------------------------------------------------

... (more tests)

============================================================
                Integration Test Summary
============================================================
  Database Connectivity      : PASSED
  Product API                : PASSED
  Recommendation Workflow    : PASSED
  Recommendation Diversity   : PASSED
  Edge Cases                 : PASSED

============================================================
✓ ALL TESTS PASSED (5/5)
```

---

### Phase 4: Quick Tests During Development

**Goal**: Fast verification during development

**Usage**:
```bash
# Test with default query
python test_ai_quick.py

# Test with custom query
python test_ai_quick.py "red formal dress"

# Test with multi-word query
python test_ai_quick.py "cotton t-shirt comfortable casual"
```

**Output**:
```
============================================================
QUICK AI RECOMMENDATION TEST
============================================================

Query: 'blue jeans casual'
------------------------------------------------------------

✓ SUCCESS: Got 5 recommendations

1. Women's Blue Denim Jeans
   Price: ₹1299
   Desc: Comfortable casual blue jeans perfect for everyday wear...

2. Ladies Casual Jeans
   Price: ₹999
   Desc: Stylish casual jeans with modern fit...

... (3 more)
```

---

### Phase 5: Run All Tests Together

**Goal**: Comprehensive test suite execution

**Run**:
```bash
cd royal_lady_backend
python run_all_ai_tests.py
```

**What Happens**:
1. Checks if model tests can run
2. Prompts to start server if needed
3. Runs all test scripts sequentially
4. Provides final summary report

**Expected Output**:
```
======================================================================
         ROYAL LADY AI - COMPREHENSIVE TEST SUITE
======================================================================

⚠ Some tests require Flask server to be running
  Please ensure 'python app.py' is running in another terminal

Press Enter when server is ready (or 'skip' to skip server tests):

Running: AI Model Components Test
Script: test_ai_model.py
----------------------------------------------------------------------
... (test output)

✓ AI Model Components Test - PASSED

----------------------------------------------------------------------

Running: API Recommendation Endpoint Test
Script: test_ai_recommendation.py
----------------------------------------------------------------------
... (test output)

✓ API Recommendation Endpoint Test - PASSED

----------------------------------------------------------------------

... (more tests)

======================================================================
                         FINAL TEST SUMMARY
======================================================================
  AI Model Components Test             : PASSED
  API Recommendation Endpoint Test     : PASSED
  End-to-End Integration Test          : PASSED

======================================================================
✓ ALL TESTS PASSED (3/3)

🎉 AI Recommendation System is fully functional!
```

---

## 🔧 Manual Testing

### Using cURL

#### 1. Basic Recommendation
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"description": "blue jeans women casual"}'
```

**Expected Response**:
```json
{
  "recommendations": [
    {
      "ProductName": "Women's Blue Denim Jeans",
      "Description": "Comfortable casual blue jeans...",
      "Price": 1299.0
    },
    ...
  ]
}
```

#### 2. Empty Query
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"description": ""}'
```

**Expected Response**:
```json
{
  "recommendations": []
}
```

#### 3. Complex Query
```bash
curl -X POST http://localhost:5000/recommend \
  -H "Content-Type: application/json" \
  -d '{"description": "elegant red dress for wedding party formal wear"}'
```

### Using Python Requests

```python
import requests

url = "http://localhost:5000/recommend"
payload = {"description": "blue jeans casual"}

response = requests.post(url, json=payload)
print(response.json())
```

### Using Postman

1. **Method**: POST
2. **URL**: `http://localhost:5000/recommend`
3. **Headers**: `Content-Type: application/json`
4. **Body** (raw JSON):
```json
{
  "description": "blue jeans women casual"
}
```
5. **Send** → Should get 5 recommendations

---

## 🐛 Troubleshooting

### Problem: Model files missing

**Error**:
```
✗ Missing: model/vectorizer.pkl
```

**Solution**:
```bash
cd royal_lady_backend/model
jupyter notebook trainer.ipynb
# Execute all cells to generate .pkl files
```

---

### Problem: Cannot connect to server

**Error**:
```
✗ Could not connect to server. Is the Flask app running?
```

**Solution**:
```bash
# In a separate terminal
cd royal_lady_backend
python app.py
```

Verify server is running by visiting: `http://localhost:5000`

---

### Problem: No recommendations returned

**Error**:
```
✓ SUCCESS: Got 0 recommendations
```

**Possible Causes**:
1. Empty `product_data.pkl`
2. Query has no matching keywords
3. Model not trained properly

**Solution**:
```bash
# Check product data
python -c "import pickle; data = pickle.load(open('model/product_data.pkl', 'rb')); print(f'Products: {len(data)}')"

# If 0, retrain model
cd model
jupyter notebook trainer.ipynb
```

---

### Problem: Import errors

**Error**:
```
ModuleNotFoundError: No module named 'sklearn'
```

**Solution**:
```bash
pip install -r requirements.txt
```

Required packages:
- Flask
- Flask-CORS
- scikit-learn
- numpy
- pandas

---

### Problem: Database not found

**Error**:
```
✗ Database connection failed
```

**Solution**:
```bash
# Check if database exists
ls ../royal.db  # or ls royal.db

# If missing, create it
cd royal_lady_backend
python app.py  # This will create the database
```

---

### Problem: Slow response time

**Symptom**: Response time >1 second

**Possible Causes**:
1. Large product dataset
2. Inefficient vectorization
3. Server overload

**Solution**:
1. Check product count:
```python
import pickle
data = pickle.load(open('model/product_data.pkl', 'rb'))
print(f'Products: {len(data)}')  # Should be reasonable (<10,000)
```

2. Profile the endpoint:
```python
import time
start = time.time()
# Make request
elapsed = time.time() - start
print(f'Time: {elapsed*1000}ms')
```

---

### Problem: Tests fail intermittently

**Symptom**: Tests pass sometimes, fail other times

**Possible Causes**:
1. Server not fully started
2. Network timeout
3. Resource contention

**Solution**:
1. Wait longer after starting server (5 seconds)
2. Increase timeout in test scripts
3. Run tests one at a time

---

## 📊 Test Results Reference

### All Green (Success) ✅

```
============================================================
                    Test Summary
============================================================
  File Existence            : PASSED
  Load Vectorizer           : PASSED
  Load Product Vectors      : PASSED
  Load Product Data         : PASSED
  Data Consistency          : PASSED
  Vectorizer Transform      : PASSED
  Recommendation Logic      : PASSED

============================================================
✓ ALL TESTS PASSED (7/7)
```

**Meaning**: AI system is fully functional and ready for production

---

### Partial Failures (Warning) ⚠️

```
============================================================
                    Test Summary
============================================================
  File Existence            : PASSED
  Load Vectorizer           : PASSED
  Load Product Vectors      : FAILED
  ...

============================================================
⚠ SOME TESTS FAILED (5/7)
```

**Meaning**: Some components need attention before deployment

---

### Complete Failure (Error) ❌

```
✗ Cannot proceed with tests. Server is not running.
```

**Meaning**: Prerequisites not met, check setup

---

## 📈 Performance Metrics

### Expected Benchmarks

| Metric | Target | Acceptable | Action Needed |
|--------|--------|------------|---------------|
| Response Time | <500ms | <1000ms | >1000ms |
| Recommendations | 5 | 3-5 | <3 |
| Success Rate | 100% | >95% | <95% |
| Relevance | High | Medium | Low |

### Measuring Performance

```bash
# Run performance test
python test_ai_recommendation.py | grep "Performance"

# Expected output:
#   Average: 234.56ms
#   Min: 123.45ms
#   Max: 456.78ms
```

---

## ✅ Pre-Deployment Checklist

Before deploying to production:

- [ ] All model files exist (3 .pkl files)
- [ ] `test_ai_model.py` passes (7/7)
- [ ] Flask server starts without errors
- [ ] `test_ai_recommendation.py` passes (7/7)
- [ ] `test_ai_integration.py` passes (5/5)
- [ ] Response time <1 second
- [ ] Tested with 10+ real user queries
- [ ] Error handling verified
- [ ] Database has sufficient products (>20)
- [ ] Documentation reviewed
- [ ] Logs checked for warnings/errors

---

## 🎓 Understanding Test Output

### Color Coding

- 🟢 **Green (✓)**: Test passed successfully
- 🔴 **Red (✗)**: Test failed, needs attention
- 🟡 **Yellow (⚠)**: Warning, may need review
- 🔵 **Blue (ℹ)**: Information, FYI only

### Common Output Patterns

**Good**:
```
✓ Request successful - Status: 200
✓ Found 5 recommendations
✓ Response time is acceptable
```

**Needs Attention**:
```
✗ Request failed - Status: 500
⚠ Response time is slow (>1s)
ℹ Expected 5 recommendations, got 3
```

---

## 📚 Additional Resources

- **Main Docs**: `PROJECT_DOCUMENTATION.md`
- **AI Testing**: `README_AI_TESTING.md`
- **Test Summary**: `AI_TEST_SUMMARY.md`
- **Model Training**: `model/trainer.ipynb`
- **API Routes**: `routes/recommend_routes.py`

---

## 🆘 Getting Help

If tests still fail after troubleshooting:

1. Check Flask logs for errors
2. Verify model files are not corrupted
3. Test with simple queries first
4. Check database has products
5. Review requirements.txt dependencies

---

**Happy Testing! 🎉**
