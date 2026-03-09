"""
Quick AI Test Script
====================

A simplified test script for quick verification of the AI recommendation system.
Perfect for quick checks during development.

Usage: python test_ai_quick.py [query]
Example: python test_ai_quick.py "blue jeans casual"
"""

import sys
import requests
import json

def test_quick(query=None):
    """Quick test of recommendation system"""
    
    if query is None:
        query = "blue jeans women casual"
    
    print("=" * 60)
    print("QUICK AI RECOMMENDATION TEST")
    print("=" * 60)
    print(f"\nQuery: '{query}'")
    print("-" * 60)
    
    url = "http://localhost:5000/recommend"
    
    try:
        response = requests.post(
            url,
            json={"description": query},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get("recommendations", [])
            
            print(f"\n✓ SUCCESS: Got {len(recommendations)} recommendations\n")
            
            for i, rec in enumerate(recommendations, 1):
                print(f"{i}. {rec.get('ProductName', 'N/A')}")
                print(f"   Price: ₹{rec.get('Price', 0)}")
                print(f"   Desc: {rec.get('Description', 'N/A')[:60]}...")
                print()
            
            return 0
        else:
            print(f"\n✗ FAILED: Status {response.status_code}")
            print(f"Response: {response.text}")
            return 1
            
    except requests.exceptions.ConnectionError:
        print("\n✗ FAILED: Cannot connect to server")
        print("Make sure Flask is running: python app.py")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        return 1


if __name__ == "__main__":
    query = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None
    exit_code = test_quick(query)
    sys.exit(exit_code)
