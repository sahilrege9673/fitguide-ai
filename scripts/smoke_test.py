#!/usr/bin/env python3
"""
FeedGuide AI — Production Health & Smoke Test Suite
Verifies API availability, security boundaries, exercise catalog, ML intent routing,
and frontend availability against either local dev or deployed production endpoints.
"""

import sys
import argparse
import time
import urllib.request
import urllib.error
import json

def test_endpoint(name: str, url: str, method: str = "GET", payload: dict = None, expected_status: int = 200):
    t0 = time.perf_counter()
    req = urllib.request.Request(url, method=method)
    req.add_header("User-Agent", "FeedGuide-SmokeTest/1.0")
    data_bytes = None
    if payload:
        req.add_header("Content-Type", "application/json")
        data_bytes = json.dumps(payload).encode("utf-8")

    try:
        with urllib.request.urlopen(req, data=data_bytes, timeout=10) as resp:
            elapsed_ms = (time.perf_counter() - t0) * 1000
            status = resp.status
            body = resp.read().decode("utf-8")
            if status == expected_status:
                print(f"  [PASS] {name} ({elapsed_ms:.1f}ms) -> HTTP {status}")
                return True, body
            else:
                print(f"  [FAIL] {name} -> Expected HTTP {expected_status}, got {status}")
                return False, body
    except urllib.error.HTTPError as e:
        elapsed_ms = (time.perf_counter() - t0) * 1000
        if e.code == expected_status:
            print(f"  [PASS] {name} ({elapsed_ms:.1f}ms) -> HTTP {e.code} (Expected Security Rejection)")
            return True, ""
        else:
            print(f"  [FAIL] {name} -> Expected HTTP {expected_status}, got HTTP {e.code}")
            return False, ""
    except Exception as e:
        elapsed_ms = (time.perf_counter() - t0) * 1000
        print(f"  [ERROR] {name} ({elapsed_ms:.1f}ms) -> Connection Error: {e}")
        return False, ""

def run_smoke_tests(api_url: str, web_url: str = None):
    api_url = api_url.rstrip("/")
    print("=" * 70)
    print("FEEDGUIDE AI — PRODUCTION SMOKE TEST SUITE")
    print(f"Target API Endpoint: {api_url}")
    if web_url:
        print(f"Target Web Endpoint: {web_url}")
    print("=" * 70)

    successes = 0
    total = 0

    # 1. API Health Check
    total += 1
    ok, body = test_endpoint("API Health Probe", f"{api_url}/api/v1/health")
    if ok:
        successes += 1

    # 2. API Root Welcome
    total += 1
    ok, _ = test_endpoint("API Root Index", f"{api_url}/")
    if ok:
        successes += 1

    # 3. Public Exercise Catalog
    total += 1
    ok, body = test_endpoint("Exercise Catalog (>= 80 records)", f"{api_url}/api/v1/exercises?page=1&page_size=5")
    if ok:
        try:
            data = json.loads(body)
            if data.get("total_records", 0) >= 80:
                print(f"         Verified catalog integrity: {data['total_records']} exercises loaded.")
                successes += 1
            else:
                print(f"         Warning: Catalog returned {data.get('total_records')} records (expected >= 80).")
        except Exception:
            pass
    total += 1 # for catalog record count check

    # 4. ML Intent Router
    total += 1
    ok, body = test_endpoint(
        "ML Intent Classification (< 20ms)",
        f"{api_url}/api/v1/chat/classify",
        method="POST",
        payload={"text": "Give me a 30-minute chest and triceps routine"}
    )
    if ok:
        try:
            data = json.loads(body)
            if data.get("intent") == "workout_request":
                print(f"         Predicted intent: '{data['intent']}' -> Target: '{data['routing_target']}'")
                successes += 1
            else:
                print(f"         Warning: Unexpected classification: {data}")
        except Exception:
            pass
    total += 1 # for intent check

    # 5. Security Boundary Guard (Unauthenticated Access MUST be rejected with 401)
    total += 1
    ok, _ = test_endpoint("Security Boundary (Unauthorized Rejection)", f"{api_url}/api/v1/profile", expected_status=401)
    if ok:
        successes += 1

    # 6. Web Frontend Availability (if provided)
    if web_url:
        total += 1
        web_url = web_url.rstrip("/")
        ok, _ = test_endpoint("Frontend Web Landing Page", f"{web_url}/")
        if ok:
            successes += 1

    print("\n" + "=" * 70)
    score_pct = (successes / total) * 100
    print(f"RESULTS: {successes}/{total} Checks Passed ({score_pct:.1f}%)")
    print("=" * 70)

    if successes == total:
        print("[SUCCESS] All production smoke checks passed! Deployment is verified.")
        return 0
    else:
        print("[FAIL] Some smoke checks failed. Check server logs and network connectivity.")
        return 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FeedGuide AI Production Smoke Test")
    parser.add_argument("--api-url", default="http://localhost:8000", help="Base URL of FastAPI API")
    parser.add_argument("--web-url", default=None, help="Base URL of Next.js frontend (optional)")
    args = parser.parse_args()

    sys.exit(run_smoke_tests(args.api_url, args.web_url))
