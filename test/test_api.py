import requests
import json

BASE_URL = "http://localhost:8386"

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert response.status_code == 200

def test_account_info():
    """Test account_info endpoint"""
    account_data = {
        "login": 10008011380,
        "password": "Schaffen2004@",
        "server": "MetaQuotes-Demo"
    }

    response = requests.post(
        f"{BASE_URL}/api/v1/account_info",
        json=account_data,
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 200

def test_history():
    """Test history endpoint"""
    history_data = {
        "login": 10008011380,
        "password": "Schaffen2004@",
        "server": "MetaQuotes-Demo",
        "from_date": "2023-01-01",
        "to_date": "2026-01-31"
    }

    response = requests.post(
        f"{BASE_URL}/api/v1/history",
        json=history_data,
        headers={'Content-Type': 'application/json'}
    )
    print(response.json())
    assert response.status_code == 200

if __name__ == "__main__":
    test_health()
    test_account_info()
    test_history()
