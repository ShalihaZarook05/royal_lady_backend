# 📑 AI Test Scripts Index

## Quick Reference Guide

This is your one-stop reference for all AI recommendation system test scripts.

---

## 📂 File Structure

```
royal_lady_backend/
├── test_ai_model.py              # Unit tests for model components
├── test_ai_recommendation.py     # API endpoint tests
├── test_ai_integration.py        # End-to-end integration tests
├── test_ai_quick.py              # Quick single-query test
├── run_all_ai_tests.py           # Master test runner
│
├── README_AI_TESTING.md          # Detailed testing documentation
├── AI_TEST_SUMMARY.md            # Test summary and overview
├── TESTING_GUIDE.md              # Complete step-by-step guide
└── TEST_SCRIPTS_INDEX.md         # This file (quick reference)
```

---

## 🎯 Which Script Should I Use?

### Scenario 1: First Time Setup
**"I just cloned the repo and want to verify everything works"**

```bash
python test_ai_model.py        # Check model files
python app.py                  # Start server (separate terminal)
python run_all_ai_tests.py    # Run all tests
```

### Scenario 2: Quick Development Check
**"I made a change and want to quickly test"**

```bash
python test_ai_quick.py "blue jeans"
```

### Scenario 3: Model Changes
**"I retrained the model and want to verify it"**

```bash
python test_ai_model.py
```

### Scenario 4: API Changes
**"I modified the /recommend endpoint"**

```bash
python test_ai_recommendation.py
```

### Scenario 5: Full Integration Check
**"I want to test the complete workflow"**

```bash
python test_ai_integration.py
```

### Scenario 6: Before Deployment
**"I want to run all tests before pushing to production"**

```bash
python run_all_ai_tests.py
```

---

## 📋 Script Details

### 1. test_ai_model.py
**Purpose**: Tests AI model components in isolation

| Aspect | Details |
|--------|---------|
| **Server Required** | ❌ No |
| **Tests** | 7 |
| **Time** | 2-3 seconds |
| **Command** | `python test_ai_model.py` |
| **Tests** | File existence, vectorizer loading, product vectors, data consistency, transformation, cosine similarity |
| **Use When** | Model files changed, first setup, debugging model issues |

---

### 2. test_ai_recommendation.py
**Purpose**: Tests the `/recommend` API endpoint

| Aspect | Details |
|--------|---------|
| **Server Required** | ✅ Yes |
| **Tests** | 7 categories |
| **Time** | 5-10 seconds |
| **Command** | `python test_ai_recommendation.py` |
| **Tests** | Server connection, basic queries, empty queries, schema validation, special characters, fashion queries, performance |
| **Use When** | API changes, endpoint testing, performance validation |

---

### 3. test_ai_integration.py
**Purpose**: End-to-end integration testing

| Aspect | Details |
|--------|---------|
| **Server Required** | ✅ Yes |
| **Database Required** | ✅ Yes |
| **Tests** | 5 categories |
| **Time** | 8-12 seconds |
| **Command** | `python test_ai_integration.py` |
| **Tests** | Database connectivity, product API, recommendation workflow, diversity, edge cases |
| **Use When** | Full system testing, before deployment, integration verification |

---

### 4. test_ai_quick.py
**Purpose**: Fast single-query testing

| Aspect | Details |
|--------|---------|
| **Server Required** | ✅ Yes |
| **Tests** | 1 query |
| **Time** | 1 second |
| **Command** | `python test_ai_quick.py "your query"` |
| **Example** | `python test_ai_quick.py "blue jeans casual"` |
| **Use When** | Quick verification during development, testing specific queries |

---

### 5. run_all_ai_tests.py
**Purpose**: Runs all test scripts sequentially

| Aspect | Details |
|--------|---------|
| **Server Required** | ✅ Yes (for some tests) |
| **Tests** | All 3 main test scripts |
| **Time** | 15-25 seconds |
| **Command** | `python run_all_ai_tests.py` |
| **Tests** | Comprehensive suite - all tests above |
| **Use When** | Pre-deployment, comprehensive validation, CI/CD pipeline |

---

## 🚦 Test Execution Order

For complete testing, run in this order:

```
1. test_ai_model.py          (No server needed)
   ↓
2. Start Flask server        (python app.py)
   ↓
3. test_ai_recommendation.py (API tests)
   ↓
4. test_ai_integration.py    (Integration tests)
   ↓
5. Review results
```

Or simply use: `python run_all_ai_tests.py` (does all above)

---

## 📊 Expected Results

### Success (All Pass) ✅

```
test_ai_model.py              → 7/7 PASSED
test_ai_recommendation.py     → 7/7 PASSED
test_ai_integration.py        → 5/5 PASSED
```

**Total**: 19/19 tests passed

### Failure Indicators ❌

- Model files missing
- Server not responding
- No recommendations returned
- Database connection failed
- Response time >1 second

---

## 🔧 Common Commands

### Run Individual Tests
```bash
# Model tests (no server needed)
python test_ai_model.py

# API tests (server required)
python test_ai_recommendation.py

# Integration tests (server + db required)
python test_ai_integration.py

# Quick test with custom query
python test_ai_quick.py "red dress formal"

# Run all tests
python run_all_ai_tests.py
```

### Start Flask Server
```bash
cd royal_lady_backend
python app.py
```

### Check Model Files
```bash
ls model/*.pkl
# Should see:
# - vectorizer.pkl
# - product_vectors.pkl
# - product_data.pkl
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 📖 Documentation Index

| Document | Purpose | When to Read |
|----------|---------|--------------|
| `TESTING_GUIDE.md` | Complete step-by-step guide | First time testing |
| `README_AI_TESTING.md` | Detailed testing documentation | In-depth understanding |
| `AI_TEST_SUMMARY.md` | High-level overview | Quick reference |
| `TEST_SCRIPTS_INDEX.md` | This file - quick reference | Need script info |

---

## 🎨 Test Output Colors

Understanding test output:

- 🟢 `✓` **Green**: Test passed
- 🔴 `✗` **Red**: Test failed
- 🟡 `⚠` **Yellow**: Warning
- 🔵 `ℹ` **Blue**: Information

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| Model files missing | Run `model/trainer.ipynb` |
| Cannot connect to server | Start Flask: `python app.py` |
| No recommendations | Check `product_data.pkl` has data |
| Import errors | Run `pip install -r requirements.txt` |
| Database not found | Ensure `royal.db` exists |

---

## 💡 Pro Tips

1. **Development**: Use `test_ai_quick.py` for rapid testing
2. **Before Commit**: Run `test_ai_model.py`
3. **Before Deploy**: Run `run_all_ai_tests.py`
4. **Debugging**: Check Flask logs while running tests
5. **Performance**: Look for "Performance Test" section in output

---

## 🔗 Related Files

### Backend Code
- `routes/recommend_routes.py` - Recommendation API endpoint
- `model/trainer.ipynb` - Model training notebook
- `app.py` - Flask application entry point

### Model Files
- `model/vectorizer.pkl` - TF-IDF vectorizer
- `model/product_vectors.pkl` - Product vectors
- `model/product_data.pkl` - Product metadata

### Configuration
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules

---

## 📈 Test Metrics

| Metric | Target | Command |
|--------|--------|---------|
| Response Time | <1s | Check in `test_ai_recommendation.py` output |
| Test Coverage | 100% | All scripts should pass |
| Success Rate | 100% | 19/19 tests |
| Recommendations | 5 per query | Verify in any test |

---

## 🎯 Quick Start Commands

```bash
# Complete test sequence (copy-paste ready)
cd royal_lady_backend

# Step 1: Test model
python test_ai_model.py

# Step 2: Start server (in new terminal)
python app.py

# Step 3: Run all tests (in original terminal)
python run_all_ai_tests.py
```

---

## 📞 Need Help?

1. Check `TESTING_GUIDE.md` for detailed troubleshooting
2. Review `README_AI_TESTING.md` for in-depth documentation
3. Look at Flask logs for error messages
4. Verify all prerequisites are met

---

**Last Updated**: 2026-01-15  
**Test Scripts Version**: 1.0  
**Total Test Coverage**: 19+ test scenarios
