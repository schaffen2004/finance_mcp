import requests
import json

BASE_URL = "http://localhost:8386"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert data.get("status") == "healthy"
    
def test_api():
    """Test API endpoints and get results"""
    print("=== Finance MCP API Test ===")

    # Test health endpoint
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/v1/health")
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")
        return

    # Test account_info endpoint
    print("\n2. Testing account_info endpoint...")
    account_data = {
        "login": 10008011380,
        "password": "Schaffen2004@",
        "server": "MetaQuotes-Demo"
    }

    try:
        response = requests.post(
            f"{BASE_URL}/api/v1/account_info",
            json=account_data,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error: {e}")

    # # Test history endpoint
    # print("\n3. Testing history endpoint...")
    # history_data = {
    #     "login": 10008011380,
    #     "password": "Schaffen2004@",
    #     "server": "MetaQuotes-Demo",
    #     "from_date": "2023-01-01",
    #     "to_date": "2026-01-01"
    # }

    # try:
    #     response = requests.post(
    #         f"{BASE_URL}/history",
    #         json=history_data,
    #         headers={'Content-Type': 'application/json'}
    #     )
    #     print(f"Status: {response.status_code}")
    #     result = response.json()
    #     print(f"Response: {json.dumps(result, indent=2)}")

    #     # Show summary if there are deals
    #     if result.get('success') and result.get('count', 0) > 0:
    #         print(f"\nSummary: Found {result['count']} deals from {result['date_range']['from_date']} to {result['date_range']['to_date']}")
    # except Exception as e:
    #     print(f"Error: {e}")

    # # Test invalid account data
    # print("\n4. Testing invalid account data...")
    # invalid_account_data = {
    #     "login": "invalid_login",
    #     "password": "test123",
    #     "server": "MetaQuotes-Demo"
    # }

    # try:
    #     response = requests.post(
    #         f"{BASE_URL}/account_info",
    #         json=invalid_account_data,
    #         headers={'Content-Type': 'application/json'}
    #     )
    #     print(f"Status: {response.status_code}")
    #     print(f"Response: {json.dumps(response.json(), indent=2)}")
    # except Exception as e:
    #     print(f"Error: {e}")

    # # Test invalid date format
    # print("\n5. Testing invalid date format...")
    # invalid_history_data = {
    #     "login": 10008011380,
    #     "password": "Schaffen2004@",
    #     "server": "MetaQuotes-Demo",
    #     "from_date": "invalid-date",
    #     "to_date": "2023-12-31"
    # }

    # try:
    #     response = requests.post(
    #         f"{BASE_URL}/history",
    #         json=invalid_history_data,
    #         headers={'Content-Type': 'application/json'}
    #     )
    #     print(f"Status: {response.status_code}")
    #     print(f"Response: {json.dumps(response.json(), indent=2)}")
    # except Exception as e:
    #     print(f"Error: {e}")

    # print("\n=== Test completed ===")

if __name__ == "__main__":
    test_health()