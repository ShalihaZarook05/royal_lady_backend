"""
Run All AI Tests
================

Master test runner that executes all AI-related tests in sequence.
Provides a comprehensive test report.
"""

import subprocess
import sys
import os

class Colors:
    HEADER = '\033[95m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


def print_banner(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text.center(70)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*70}{Colors.ENDC}\n")


def run_test_script(script_name, description):
    """Run a test script and return success status"""
    print(f"\n{Colors.BOLD}Running: {description}{Colors.ENDC}")
    print(f"Script: {script_name}")
    print("-" * 70)
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=False,
            text=True
        )
        
        success = result.returncode == 0
        
        if success:
            print(f"\n{Colors.OKGREEN}✓ {description} - PASSED{Colors.ENDC}")
        else:
            print(f"\n{Colors.FAIL}✗ {description} - FAILED{Colors.ENDC}")
        
        return success
        
    except FileNotFoundError:
        print(f"{Colors.FAIL}✗ Script not found: {script_name}{Colors.ENDC}")
        return False
    except Exception as e:
        print(f"{Colors.FAIL}✗ Error running {script_name}: {str(e)}{Colors.ENDC}")
        return False


def main():
    """Run all AI test scripts"""
    print_banner("ROYAL LADY AI - COMPREHENSIVE TEST SUITE")
    
    # Change to backend directory if needed
    if not os.path.exists("model"):
        if os.path.exists("royal_lady_backend"):
            os.chdir("royal_lady_backend")
            print(f"{Colors.OKGREEN}Changed to royal_lady_backend directory{Colors.ENDC}\n")
    
    test_suite = [
        {
            "script": "test_ai_model.py",
            "description": "AI Model Components Test",
            "required": True,
            "requires_server": False
        },
        {
            "script": "test_ai_recommendation.py",
            "description": "API Recommendation Endpoint Test",
            "required": True,
            "requires_server": True
        },
        {
            "script": "test_ai_integration.py",
            "description": "End-to-End Integration Test",
            "required": True,
            "requires_server": True
        }
    ]
    
    results = {}
    
    # Check if server is needed and running
    server_needed = any(test["requires_server"] for test in test_suite)
    
    if server_needed:
        print(f"{Colors.WARNING}⚠ Some tests require Flask server to be running{Colors.ENDC}")
        print(f"{Colors.WARNING}  Please ensure 'python app.py' is running in another terminal{Colors.ENDC}")
        
        response = input(f"\n{Colors.BOLD}Press Enter when server is ready (or 'skip' to skip server tests): {Colors.ENDC}")
        
        if response.lower() == 'skip':
            print(f"{Colors.WARNING}Skipping tests that require server{Colors.ENDC}")
            test_suite = [t for t in test_suite if not t["requires_server"]]
    
    # Run all tests
    for test in test_suite:
        success = run_test_script(test["script"], test["description"])
        results[test["description"]] = success
        
        if not success and test["required"]:
            print(f"\n{Colors.WARNING}⚠ Required test failed. Continuing with remaining tests...{Colors.ENDC}")
    
    # Print final summary
    print_banner("FINAL TEST SUMMARY")
    
    passed = sum(1 for success in results.values() if success)
    total = len(results)
    
    for test_name, success in results.items():
        status = f"{Colors.OKGREEN}PASSED{Colors.ENDC}" if success else f"{Colors.FAIL}FAILED{Colors.ENDC}"
        print(f"  {test_name.ljust(40)} : {status}")
    
    print(f"\n{Colors.BOLD}{'='*70}{Colors.ENDC}")
    
    if passed == total:
        print(f"{Colors.OKGREEN}{Colors.BOLD}✓ ALL TESTS PASSED ({passed}/{total}){Colors.ENDC}")
        print(f"\n{Colors.OKGREEN}🎉 AI Recommendation System is fully functional!{Colors.ENDC}\n")
        return 0
    else:
        failed = total - passed
        print(f"{Colors.WARNING}{Colors.BOLD}⚠ {failed} TEST(S) FAILED ({passed}/{total} passed){Colors.ENDC}")
        print(f"\n{Colors.WARNING}Please review the failed tests above.{Colors.ENDC}\n")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
