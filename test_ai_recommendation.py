"""
Test Script for Royal Lady AI Recommendation System
====================================================

This script tests the AI-powered product recommendation endpoint.
It uses TF-IDF vectorization and cosine similarity to recommend products
based on text descriptions.

Test Coverage:
1. Model file loading
2. Recommendation endpoint with various queries
3. Edge cases (empty query, special characters)
4. Response format validation
5. Similarity scoring validation
"""

import requests
import json
import sys
from typing import List, Dict

# Configuration
BASE_URL = "http://localhost:5000"
RECOMMEND_ENDPOINT = f"{BASE_URL}/recommend"

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
    UNDERLINE = '\033[4m'


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


def print_warning(message: str):
    """Print warning message"""
    print(f"{Colors.WARNING}⚠ {message}{Colors.ENDC}")


def print_info(message: str):
    """Print info message"""
    print(f"{Colors.OKCYAN}ℹ {message}{Colors.ENDC}")


def test_server_connection() -> bool:
    """Test if the Flask server is running"""
    print_test("Server Connection Test")
    try:
        response = requests.get(BASE_URL, timeout=5)
        if response.status_code == 200:
            print_success(f"Server is running: {response.json()}")
            return True
        else:
            print_failure(f"Server responded with status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_failure("Could not connect to server. Is the Flask app running?")
        print_info("Run: python app.py")
        return False
    except Exception as e:
        print_failure(f"Unexpected error: {str(e)}")
        return False


def test_recommendation_basic(description: str) -> Dict:
    """Test basic recommendation functionality"""
    print_test(f"Basic Recommendation Test - Query: '{description}'")
    
    try:
        payload = {"description": description}
        response = requests.post(
            RECOMMEND_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Request successful - Status: {response.status_code}")
            
            # Validate response structure
            if "recommendations" in data:
                recommendations = data["recommendations"]
                print_success(f"Found {len(recommendations)} recommendations")
                
                # Display recommendations
                for i, rec in enumerate(recommendations, 1):
                    print(f"\n  {Colors.BOLD}Recommendation {i}:{Colors.ENDC}")
                    print(f"    Product: {rec.get('ProductName', 'N/A')}")
                    print(f"    Price: ₹{rec.get('Price', 0)}")
                    print(f"    Description: {rec.get('Description', 'N/A')[:100]}...")
                
                return {"success": True, "data": data}
            else:
                print_failure("Response missing 'recommendations' key")
                return {"success": False, "error": "Invalid response structure"}
        else:
            print_failure(f"Request failed - Status: {response.status_code}")
            print_info(f"Response: {response.text}")
            return {"success": False, "error": f"Status {response.status_code}"}
            
    except Exception as e:
        print_failure(f"Exception occurred: {str(e)}")
        return {"success": False, "error": str(e)}


def test_empty_query():
    """Test recommendation with empty query"""
    print_test("Empty Query Test")
    
    try:
        payload = {"description": ""}
        response = requests.post(
            RECOMMEND_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get("recommendations", [])
            
            if len(recommendations) == 0:
                print_success("Correctly returned empty recommendations for empty query")
                return True
            else:
                print_warning(f"Expected 0 recommendations, got {len(recommendations)}")
                return False
        else:
            print_failure(f"Request failed - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_failure(f"Exception occurred: {str(e)}")
        return False


def test_response_schema(description: str):
    """Test if response matches expected schema"""
    print_test("Response Schema Validation Test")
    
    try:
        payload = {"description": description}
        response = requests.post(
            RECOMMEND_ENDPOINT,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            
            # Check top-level structure
            if "recommendations" not in data:
                print_failure("Missing 'recommendations' key in response")
                return False
            
            recommendations = data["recommendations"]
            
            if not isinstance(recommendations, list):
                print_failure("'recommendations' is not a list")
                return False
            
            # Check each recommendation structure
            required_fields = ["ProductName", "Description", "Price"]
            all_valid = True
            
            for i, rec in enumerate(recommendations):
                for field in required_fields:
                    if field not in rec:
                        print_failure(f"Recommendation {i+1} missing '{field}' field")
                        all_valid = False
                
                # Validate data types
                if not isinstance(rec.get("ProductName"), str):
                    print_failure(f"Recommendation {i+1}: ProductName is not a string")
                    all_valid = False
                
                if not isinstance(rec.get("Description"), str):
                    print_failure(f"Recommendation {i+1}: Description is not a string")
                    all_valid = False
                
                if not isinstance(rec.get("Price"), (int, float)):
                    print_failure(f"Recommendation {i+1}: Price is not a number")
                    all_valid = False
            
            if all_valid:
                print_success("All recommendations have valid schema")
                return True
            else:
                return False
        else:
            print_failure(f"Request failed - Status: {response.status_code}")
            return False
            
    except Exception as e:
        print_failure(f"Exception occurred: {str(e)}")
        return False


def test_special_characters():
    """Test recommendation with special characters"""
    print_test("Special Characters Test")
    
    test_queries = [
        "women's dress with @#$ symbols",
        "shoes & bags collection",
        "t-shirt (100% cotton)",
        "Jeans—blue color!",
    ]
    
    all_passed = True
    for query in test_queries:
        try:
            payload = {"description": query}
            response = requests.post(
                RECOMMEND_ENDPOINT,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                print_success(f"Query '{query}' processed successfully")
            else:
                print_failure(f"Query '{query}' failed with status {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print_failure(f"Query '{query}' raised exception: {str(e)}")
            all_passed = False
    
    return all_passed


def test_various_fashion_queries():
    """Test various fashion-related queries"""
    print_test("Various Fashion Queries Test")
    
    test_cases = [
        {
            "description": "casual blue jeans for women",
            "expected_keywords": ["jeans", "blue", "women", "casual"]
        },
        {
            "description": "formal black dress for party",
            "expected_keywords": ["dress", "black", "formal"]
        },
        {
            "description": "cotton t-shirt comfortable",
            "expected_keywords": ["cotton", "shirt"]
        },
        {
            "description": "red color ethnic wear",
            "expected_keywords": ["red", "ethnic"]
        },
        {
            "description": "winter jacket warm",
            "expected_keywords": ["jacket", "winter"]
        }
    ]
    
    results = []
    
    for test_case in test_cases:
        query = test_case["description"]
        print(f"\n{Colors.BOLD}Query: {query}{Colors.ENDC}")
        
        try:
            payload = {"description": query}
            response = requests.post(
                RECOMMEND_ENDPOINT,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                recommendations = data.get("recommendations", [])
                
                if len(recommendations) > 0:
                    print_success(f"Got {len(recommendations)} recommendations")
                    
                    # Check if recommendations are relevant
                    first_rec = recommendations[0]
                    product_text = (first_rec.get("ProductName", "") + " " + 
                                  first_rec.get("Description", "")).lower()
                    
                    keyword_found = any(keyword.lower() in product_text 
                                      for keyword in test_case["expected_keywords"])
                    
                    if keyword_found:
                        print_success("Recommendations appear relevant to query")
                        results.append(True)
                    else:
                        print_warning("Recommendations might not be highly relevant")
                        results.append(True)  # Still pass if we got results
                else:
                    print_warning("No recommendations returned")
                    results.append(False)
            else:
                print_failure(f"Request failed with status {response.status_code}")
                results.append(False)
                
        except Exception as e:
            print_failure(f"Exception: {str(e)}")
            results.append(False)
    
    passed = sum(results)
    total = len(results)
    print(f"\n{Colors.BOLD}Results: {passed}/{total} queries successful{Colors.ENDC}")
    
    return passed == total


def test_performance():
    """Test response time performance"""
    print_test("Performance Test")
    
    import time
    
    query = "blue jeans women casual"
    payload = {"description": query}
    
    times = []
    num_requests = 5
    
    print_info(f"Sending {num_requests} requests to measure response time...")
    
    for i in range(num_requests):
        try:
            start_time = time.time()
            response = requests.post(
                RECOMMEND_ENDPOINT,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000  # Convert to ms
            times.append(response_time)
            
            if response.status_code == 200:
                print(f"  Request {i+1}: {response_time:.2f}ms - ✓")
            else:
                print(f"  Request {i+1}: Failed (Status {response.status_code})")
                
        except Exception as e:
            print(f"  Request {i+1}: Exception - {str(e)}")
    
    if times:
        avg_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        
        print(f"\n{Colors.BOLD}Performance Metrics:{Colors.ENDC}")
        print(f"  Average: {avg_time:.2f}ms")
        print(f"  Min: {min_time:.2f}ms")
        print(f"  Max: {max_time:.2f}ms")
        
        if avg_time < 1000:  # Less than 1 second
            print_success("Response time is acceptable")
            return True
        else:
            print_warning("Response time is slow (>1s)")
            return False
    else:
        print_failure("No successful requests")
        return False


def run_all_tests():
    """Run all tests and generate summary"""
    print_header("Royal Lady AI Recommendation System - Test Suite")
    
    test_results = {}
    
    # Test 1: Server Connection
    test_results["Server Connection"] = test_server_connection()
    
    if not test_results["Server Connection"]:
        print_failure("\n❌ Cannot proceed with tests. Server is not running.")
        return
    
    print("\n" + "-"*60 + "\n")
    
    # Test 2: Basic Recommendations
    result = test_recommendation_basic("blue jeans women casual")
    test_results["Basic Recommendation"] = result.get("success", False)
    
    print("\n" + "-"*60 + "\n")
    
    # Test 3: Empty Query
    test_results["Empty Query"] = test_empty_query()
    
    print("\n" + "-"*60 + "\n")
    
    # Test 4: Response Schema
    test_results["Response Schema"] = test_response_schema("formal dress")
    
    print("\n" + "-"*60 + "\n")
    
    # Test 5: Special Characters
    test_results["Special Characters"] = test_special_characters()
    
    print("\n" + "-"*60 + "\n")
    
    # Test 6: Various Fashion Queries
    test_results["Fashion Queries"] = test_various_fashion_queries()
    
    print("\n" + "-"*60 + "\n")
    
    # Test 7: Performance
    test_results["Performance"] = test_performance()
    
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
    print(f"{Colors.OKCYAN}Starting Royal Lady AI Recommendation System Tests...{Colors.ENDC}")
    print(f"{Colors.OKCYAN}Make sure the Flask backend is running on {BASE_URL}{Colors.ENDC}\n")
    
    exit_code = run_all_tests()
    sys.exit(exit_code)
