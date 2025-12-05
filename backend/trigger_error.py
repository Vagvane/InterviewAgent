import requests
import json

url = "http://localhost:8000/api/v1/assessment/daily?refresh=true"
print(f"Requesting {url}...")

try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    try:
        print("Response Body:")
        print(json.dumps(response.json(), indent=2))
    except:
        print(f"Raw Response: {response.text}")
except Exception as e:
    print(f"Request Failed: {e}")
