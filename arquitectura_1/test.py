import requests
import time

BASE_URL = "http://localhost:8000"

# Test 1
print("=== Test 1: Create Short URL ===")
response = requests.post(
    f"{BASE_URL}/url_shortener",
    json={"url_long": "https://www.example.com/very/long/url"}
)
print(f"Status: {response.status_code}")
result = response.json()
print(f"Result: {result}")
short_hash = result["hash"]

# Test 2
print("\n=== Test 2: Access Short URL (HTTP 302 Redirect) ===")
response = requests.get(
    f"{BASE_URL}/url_shortener/{short_hash}",
    allow_redirects=False
)
print(f"Status: {response.status_code}")
print(f"Location Header: {response.headers.get('Location')}")
print(f"Cache-Control: {response.headers.get('Cache-Control')}")