#!/usr/bin/env python3
import json
import requests
import time
import argparse
from datetime import datetime

def load_config(path):
    with open(path, 'r') as f:
        return json.load(f)

def execute_test(test):
    url = test.get("endpoint", "http://localhost:8080")
    method = test.get("method", "GET").upper()
    payload = test.get("payload", {})
    headers = test.get("headers", {})
    expected_status = test.get("expected_status_code", None)

    try:
        response = requests.request(method, url, json=payload, headers=headers, timeout=5)
        status_ok = (response.status_code == expected_status)
        return {
            "id": test["id"],
            "name": test["name"],
            "status": "PASS" if status_ok else "FAIL",
            "expected": expected_status,
            "received": response.status_code,
            "time": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        return {
            "id": test["id"],
            "name": test["name"],
            "status": "ERROR",
            "error": str(e),
            "time": datetime.utcnow().isoformat() + "Z"
        }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, help="Path to fuzzing test config JSON")
    args = parser.parse_args()

    config = load_config(args.config)
    tests = config.get("testcases", [])
    results = []

    print(f"[*] Starting API fuzzing with {len(tests)} test cases...")

    for test in tests:
        result = execute_test(test)
        results.append(result)
        print(f"[+] {result['id']} {result['name']} → {result['status']}")

    out_path = "fuzzing-results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=4)

    print(f"
[✔] Results saved to {out_path}")

if __name__ == "__main__":
    main()
