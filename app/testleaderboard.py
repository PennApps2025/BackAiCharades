# test_leaderboard.py
import requests

BASE_URL = "http://localhost:8000"  # FastAPI 서버 주소

#  POST data
test_entries = [
    {"username": "Alice", "score": 8},
    {"username": "Bob", "score": 10},
    {"username": "Charlie", "score": 6},
    {"username": "Dave", "score": 9},
    {"username": "Eve", "score": 7},
]

# # 1. POST request
# for entry in test_entries:
#     response = requests.post(f"{BASE_URL}/leaderboard", json=entry)
#     if response.status_code == 200:
#         print(f"Successfully added: {entry}")
#     else:
#         print(f"Failed to add {entry}: {response.text}")

# 2. GET request
response = requests.get(f"{BASE_URL}/leaderboard")
if response.status_code == 200:
    print("\nTop Leaderboard Entries:")
    for entry in response.json():
        print(entry)
else:
    print("Failed to fetch leaderboard:", response.text)
