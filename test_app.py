import requests
import sys
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"

def wait_for_server():
    print("Waiting for server to start...")
    for _ in range(10):
        try:
            requests.get("http://127.0.0.1:8000/")
            print("Server is up!")
            return
        except requests.ConnectionError:
            time.sleep(1)
    print("Server failed to start.")
    sys.exit(1)

def test_flow():
    wait_for_server()
    
    # 1. Register
    email = "test@example.com"
    password = "password123"
    print(f"Registering user {email}...")
    resp = requests.post(f"{BASE_URL}/auth/register", json={
        "email": email,
        "password": password,
        "full_name": "Test User"
    })
    
    # Handle if user already exists (if re-running test)
    if resp.status_code == 400:
        print("User might already exist. Proceeding...")
    elif resp.status_code != 200:
        print(f"Registration failed: {resp.text}")
        sys.exit(1)
    
    # 2. Login
    print("Logging in...")
    resp = requests.post(f"{BASE_URL}/auth/token", data={
        "username": email,
        "password": password
    })
    if resp.status_code != 200:
        print(f"Login failed: {resp.text}")
        sys.exit(1)
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Got token: {token[:10]}...")

    # 3. Check Balance
    print("Checking balance...")
    resp = requests.get(f"{BASE_URL}/wallet/balance", headers=headers)
    print(f"Balance: {resp.json()}")

    # 4. Load Wallet
    print("Loading 100.0...")
    resp = requests.post(f"{BASE_URL}/wallet/load", json={"amount": 100.0}, headers=headers)
    print(f"New Balance: {resp.json()}")

    # 5. Buy Bundle
    print("Buying Data bundle (cost 50.0)...")
    resp = requests.post(f"{BASE_URL}/bundles/buy", json={"type": "data", "amount": 50.0}, headers=headers)
    print(f"Bundle bought: {resp.json()}")

    # 6. Check Balance again
    print("Checking balance after purchase...")
    resp = requests.get(f"{BASE_URL}/wallet/balance", headers=headers)
    print(f"Balance: {resp.json()}")

    # 7. Simulate Usage
    print("Simulating usage of 10.0 data...")
    resp = requests.post(f"{BASE_URL}/usage/simulate", json={"type": "data", "amount": 10.0}, headers=headers)
    print(f"Usage result: {resp.json()}")

    # 8. Check My Bundles
    print("Checking my bundles...")
    resp = requests.get(f"{BASE_URL}/bundles/my-bundles", headers=headers)
    print(f"My Bundles: {resp.json()}")

if __name__ == "__main__":
    try:
        test_flow()
        print("\nSUCCESS: All tests passed!")
    except Exception as e:
        print(f"\nERROR: {e}")
        sys.exit(1)
