"""
Test Script for AI Model Files
===============================

This script tests the AI model components (pickle files) directly
without running the Flask server. It validates:
1. Model file existence and loading
2. Vectorizer functionality
3. Product vectors integrity
4. Product data structure
5. Cosine similarity calculations
"""

import pickle
import os
import sys
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class Colors:
    """Terminal colors for better output visibility"""
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_header(text: str):
    """Print formatted header"""
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")


def print_test(test_name: str):
    """Print test name"""
    print(f"{Colors.OKBLUE}{Colors.BOLD}TEST: {test_name}{Colors.ENDC}")


def print_success(message: str):
    """Print success message"""
    print(f"{Colors.OKGREEN}✓ {message}{Colors.ENDC}")


def print_failure(message: str):
    """Print failure message"""
    print(f"{Colors.FAIL}✗ {message}{Colors.ENDC}")


def print_info(message: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")


def test_model_files_exist():
    """Test if all required model files exist"""
    print_test("Model Files Existence Check")
    
    required_files = [
        "model/vectorizer.pkl",
        "model/product_vectors.pkl",
        "model/product_data.pkl"
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print_success(f"Found: {file_path} ({file_size} bytes)")
        else:
            print_failure(f"Missing: {file_path}")
            all_exist = False
    
    return all_exist


def test_load_vectorizer():
    """Test loading the TF-IDF vectorizer"""
    print_test("Loading Vectorizer")
    
    try:
        with open("model/vectorizer.pkl", "rb") as f:
            vectorizer = pickle.load(f)
        
        print_success("Vectorizer loaded successfully")
        print_info(f"Type: {type(vectorizer).__name__}")
        
        # Check if it has transform method
        if hasattr(vectorizer, 'transform'):
            print_success("Vectorizer has 'transform' method")
        else:
            print_failure("Vectorizer missing 'transform' method")
            return None
        
        # Try to get vocabulary size
        if hasattr(vectorizer, 'vocabulary_'):
            vocab_size = len(vectorizer.vocabulary_)
            print_info(f"Vocabulary size: {vocab_size} words")
        
        return vectorizer
        
    except Exception as e:
        print_failure(f"Failed to load vectorizer: {str(e)}")
        return None


def test_load_product_vectors():
    """Test loading product vectors"""
    print_test("Loading Product Vectors")
    
    try:
        with open("model/product_vectors.pkl", "rb") as f:
            product_vectors = pickle.load(f)
        
        print_success("Product vectors loaded successfully")
        print_info(f"Type: {type(product_vectors)}")
        print_info(f"Shape: {product_vectors.shape}")
        print_info(f"Number of products: {product_vectors.shape[0]}")
        print_info(f"Vector dimension: {product_vectors.shape[1]}")
        
        return product_vectors
        
    except Exception as e:
        print_failure(f"Failed to load product vectors: {str(e)}")
        return None


def test_load_product_data():
    """Test loading product data"""
    print_test("Loading Product Data")
    
    try:
        with open("model/product_data.pkl", "rb") as f:
            product_data = pickle.load(f)
        
        print_success("Product data loaded successfully")
        print_info(f"Type: {type(product_data)}")
        print_info(f"Number of products: {len(product_data)}")
        
        # Check structure of first product
        if len(product_data) > 0:
            first_product = product_data[0]
            print_info(f"First product keys: {list(first_product.keys())}")
            print_info(f"Sample product: {first_product.get('ProductName', 'N/A')}")
        
        return product_data
        
    except Exception as e:
        print_failure(f"Failed to load product data: {str(e)}")
        return None


def test_vectorizer_transform(vectorizer):
    """Test vectorizer transformation"""
    print_test("Vectorizer Transformation Test")
    
    if vectorizer is None:
        print_failure("Vectorizer not loaded, skipping test")
        return False
    
    test_queries = [
        "blue jeans women casual",
        "formal black dress party",
        "cotton t-shirt comfortable",
        "red ethnic wear traditional"
    ]
    
    try:
        for query in test_queries:
            vector = vectorizer.transform([query])
            print_success(f"Transformed: '{query}'")
            print_info(f"  Vector shape: {vector.shape}")
            print_info(f"  Non-zero elements: {vector.nnz}")
        
        return True
        
    except Exception as e:
        print_failure(f"Transformation failed: {str(e)}")
        return False


def test_recommendation_logic(vectorizer, product_vectors, product_data):
    """Test the complete recommendation logic"""
    print_test("Complete Recommendation Logic Test")
    
    if any(x is None for x in [vectorizer, product_vectors, product_data]):
        print_failure("Required components not loaded, skipping test")
        return False
    
    test_query = "blue casual jeans for women"
    
    try:
        # Step 1: Vectorize input
        print_info(f"Query: '{test_query}'")
        input_vec = vectorizer.transform([test_query])
        print_success("Step 1: Input vectorized")
        
        # Step 2: Calculate cosine similarity
        similarity_scores = cosine_similarity(input_vec, product_vectors)[0]
        print_success(f"Step 2: Similarity scores calculated ({len(similarity_scores)} scores)")
        print_info(f"  Min score: {similarity_scores.min():.4f}")
        print_info(f"  Max score: {similarity_scores.max():.4f}")
        print_info(f"  Mean score: {similarity_scores.mean():.4f}")
        
        # Step 3: Get top 5 recommendations
        top_indices = similarity_scores.argsort()[-5:][::-1]
        print_success(f"Step 3: Top 5 indices retrieved: {top_indices.tolist()}")
        
        # Step 4: Display recommendations
        print(f"\n{Colors.BOLD}Top 5 Recommendations:{Colors.ENDC}")
        for i, idx in enumerate(top_indices, 1):
            product = product_data[idx]
            score = similarity_scores[idx]
            print(f"\n  {Colors.BOLD}Rank {i} (Similarity: {score:.4f}):{Colors.ENDC}")
            print(f"    Product: {product.get('ProductName', 'N/A')}")
            print(f"    Price: ₹{product.get('Price', 0)}")
            print(f"    Description: {product.get('Description', 'N/A')[:80]}...")
        
        return True
        
    except Exception as e:
        print_failure(f"Recommendation logic failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def test_data_consistency(product_vectors, product_data):
    """Test consistency between vectors and data"""
    print_test("Data Consistency Check")
    
    if product_vectors is None or product_data is None:
        print_failure("Data not loaded, skipping test")
        return False
    
    vector_count = product_vectors.shape[0]
    data_count = len(product_data)
    
    if vector_count == data_count:
        print_success(f"Data is consistent: {vector_count} products in both vectors and data")
        return True
    else:
        print_failure(f"Data mismatch: {vector_count} vectors vs {data_count} data entries")
        return False


def run_all_tests():
    """Run all model tests"""
    print_header("AI Model Components Test Suite")
    
    test_results = {}
    
    # Test 1: Check file existence
    test_results["File Existence"] = test_model_files_exist()
    
    if not test_results["File Existence"]:
        print_failure("\n❌ Model files missing. Run trainer.ipynb first.")
        return 1
    
    print("\n" + "-"*60 + "\n")
    
    # Test 2: Load vectorizer
    vectorizer = test_load_vectorizer()
    test_results["Load Vectorizer"] = vectorizer is not None
    
    print("\n" + "-"*60 + "\n")
    
    # Test 3: Load product vectors
    product_vectors = test_load_product_vectors()
    test_results["Load Product Vectors"] = product_vectors is not None
    
    print("\n" + "-"*60 + "\n")
    
    # Test 4: Load product data
    product_data = test_load_product_data()
    test_results["Load Product Data"] = product_data is not None
    
    print("\n" + "-"*60 + "\n")
    
    # Test 5: Data consistency
    test_results["Data Consistency"] = test_data_consistency(product_vectors, product_data)
    
    print("\n" + "-"*60 + "\n")
    
    # Test 6: Vectorizer transformation
    test_results["Vectorizer Transform"] = test_vectorizer_transform(vectorizer)
    
    print("\n" + "-"*60 + "\n")
    
    # Test 7: Complete recommendation logic
    test_results["Recommendation Logic"] = test_recommendation_logic(
        vectorizer, product_vectors, product_data
    )
    
    # Print Summary
    print_header("Test Summary")
    
    passed = sum(1 for result in test_results.values() if result)
    total = len(test_results)
    
    for test_name, result in test_results.items():
        status = f"{Colors.OKGREEN}PASSED{Colors.ENDC}" if result else f"{Colors.FAIL}FAILED{Colors.ENDC}"
        print(f"  {test_name.ljust(25)} : {status}")
    
    print(f"\n{Colors.BOLD}{'='*60}{Colors.ENDC}")
    
    if passed == total:
        print(f"{Colors.OKGREEN}{Colors.BOLD}✓ ALL TESTS PASSED ({passed}/{total}){Colors.ENDC}")
        return 0
    else:
        print(f"{Colors.WARNING}{Colors.BOLD}⚠ SOME TESTS FAILED ({passed}/{total}){Colors.ENDC}")
        return 1


if __name__ == "__main__":
    # Change to backend directory if needed
    if not os.path.exists("model"):
        print_info("Changing to royal_lady_backend directory...")
        if os.path.exists("royal_lady_backend"):
            os.chdir("royal_lady_backend")
    
    exit_code = run_all_tests()
    sys.exit(exit_code)
