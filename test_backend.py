import requests
import json

url = "http://localhost:8000/chat"
payload = {
    "message": "Hello AI, are you active?",
    "model": "tinyllama"
}
headers = {
    "Content-Type": "application/json"
}

try:
    response = requests.post(url, data=json.dumps(payload), headers=headers, timeout=30)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
except Exception as e:
    print(f"Error: {e}")
