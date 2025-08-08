import requests
import json
import urllib3

# Disable insecure request warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Ngrok or local FastAPI endpoint
url = "https://119c8fa4bb9e.ngrok-free.app/api/v1/hackrx/run"

# Payload
payload = {
    "documents": ["This is a sample document about DevOps and continuous integration practices."],
    "questions": ["What is DevOps?", "Explain CI/CD pipeline"]
}

print("🚀 Testing webhook endpoint...")
print(f"URL: {url}")
print(f"Payload: {json.dumps(payload, indent=2)}")

try:
    response = requests.post(
        url,
        json=payload,
        headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        verify=False,  # <--- THIS LINE FIXES SSL ERROR
        proxies={"http": None, "https": None}
    )

    print("\n✅ Response:")
    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        try:
            result = response.json()
            print("Response JSON:")
            print(json.dumps(result, indent=2))
        except json.JSONDecodeError:
            print("Response Text:")
            print(response.text)
    else:
        print(f"❌ Error Response: {response.status_code}")
        print("Response Text:")
        print(response.text)

except requests.exceptions.RequestException as e:
    print(f"❌ Request failed: {e}")
    print("\n💡 Make sure your FastAPI server is running:")
    print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    print("\n💡 For ngrok testing:")
    print("   1. Start your server: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
    print("   2. Start ngrok: ngrok http 8000")
    print("   3. Update the URL in this file with your ngrok URL")
