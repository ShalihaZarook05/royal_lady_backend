# AI Recommendation Integration Test Suite

import requests
import sqlite3
import os
import sys

# ---------------- PRINT HELPERS ----------------
def header(text):
    print("\n" + "="*60)
    print(text.center(60))
    print("="*60)

def ok(msg):
    print("✓", msg)

def fail(msg):
    print("✗", msg)

def info(msg):
    print("•", msg)

# ---------------- DATABASE TEST ----------------
def test_database():
    print("\nTEST 1 — Database Connectivity")

    db_path = os.path.join(os.path.dirname(__file__), "database", "royal.db")

    if not os.path.exists(db_path):
        fail("Database file not found")
        return False

    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cur.fetchall()

        ok("Database opened")
        info("Tables: " + ", ".join(t[0] for t in tables))

        conn.close()
        return True

    except Exception as e:
        fail(str(e))
        return False

# ---------------- API TEST ----------------
def test_api():
    print("\nTEST 2 — Flask API")

    try:
        r = requests.get("http://127.0.0.1:5000/", timeout=5)
        if r.status_code == 200:
            ok("API reachable")
            return True
        else:
            fail("API returned status " + str(r.status_code))
            return False
    except:
        fail("Flask not running")
        return False

# ---------------- RECOMMEND TEST ----------------
def test_recommend():
    print("\nTEST 3 — Recommendation")

    queries = ["red saree", "cotton saree", "party silk saree"]
    success = True

    for q in queries:
        try:
            r = requests.post(
                "http://127.0.0.1:5000/recommend",
                json={"description": q},
                timeout=10
            )
            data = r.json()

            if data.get("recommendations"):
                ok(f"{q} → {data['recommendations'][0]['ProductName']}")
            else:
                fail(q)
                success = False
        except:
            fail(q)
            success = False

    return success

# ---------------- RUN ALL ----------------
def main():
    header("AI RECOMMENDATION SYSTEM TEST")

    results = []
    results.append(test_database())
    results.append(test_api())
    results.append(test_recommend())

    header("SUMMARY")

    passed = sum(results)
    total = len(results)

    print(f"Passed: {passed}/{total}")

    if passed == total:
        print("ALL TESTS PASSED")
    else:
        print("SOME TESTS FAILED")

# ENTRY POINT
if __name__ == "__main__":
    main()
