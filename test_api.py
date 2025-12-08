import requests
import json

def test_endpoint(endpoint):
    try:
        url = f"http://localhost:8000{endpoint}"
        print(f"\n🔍 Testing {endpoint}...")
        
        if endpoint == "/api/ask":
            response = requests.post(url, json={"question": "سلام"})
        else:
            response = requests.get(url)
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Response:")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return True
        else:
            print(f"❌ Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

if __name__ == "__main__":
    endpoints = ["/", "/api/health", "/api/knowledge", "/api/debug", "/api/ask"]
    
    print("🚀 Starting API Tests...")
    results = []
    
    for endpoint in endpoints:
        success = test_endpoint(endpoint)
        results.append((endpoint, success))
    
    print("\n📋 Test Summary:")
    print("=" * 40)
    for endpoint, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{endpoint:20} {status}")
    
    # Check if all passed
    if all(success for _, success in results):
        print("\n🎉 All tests passed! System is healthy.")
    else:
        print("\n⚠️ Some tests failed. Please check the API.")
