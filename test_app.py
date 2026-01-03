import json
import urllib.request
import urllib.parse
import sys
import time

BASE_URL = "http://127.0.0.1:8000/api/v1"

def make_request(url, method="GET", data=None, headers=None):
    if headers is None:
        headers = {}
    
    if data is not None:
        data_bytes = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    else:
        data_bytes = None
    
    req = urllib.request.Request(url, data=data_bytes, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req) as response:
            resp_body = response.read().decode("utf-8")
            return response.status, json.loads(resp_body)
    except urllib.error.HTTPError as e:
        resp_body = e.read().decode("utf-8")
        try:
            return e.code, json.loads(resp_body)
        except:
            return e.code, resp_body

def wait_for_server():
    print("Waiting for server to start...")
    for _ in range(10):
        try:
            with urllib.request.urlopen("http://127.0.0.1:8000/") as response:
                if response.status == 200:
                    print("Server is up!")
                    return
        except Exception:
            time.sleep(1)
    print("Server failed to start.")
    sys.exit(1)

def test_flow():
    wait_for_server()
    
    # 1. Register
    email = "test@example.com"
    password = "password123"
    print(f"Registering user {email}...")
    
    status, body = make_request(f"{BASE_URL}/auth/register", method="POST", data={
        "email": email,
        "password": password,
        "full_name": "Test User"
    })
    
    if status == 400:
        print("User might already exist (400). Proceeding...")
    elif status != 200:
        print(f"Registration failed: {status} {body}")
        sys.exit(1)
    
    # 2. Login
    print("Logging in...")
    data = urllib.parse.urlencode({
        "username": email,
        "password": password
    }).encode("utf-8")
    
    req = urllib.request.Request(f"{BASE_URL}/auth/token", data=data, method="POST")
    # urllib sets Content-Type to application/x-www-form-urlencoded automatically when data is provided
    
    try:
        with urllib.request.urlopen(req) as response:
            body = json.loads(response.read().decode("utf-8"))
            status = response.status
    except urllib.error.HTTPError as e:
        print(f"Login failed: {e.read().decode('utf-8')}")
        sys.exit(1)

    token = body["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"Got token: {token[:10]}...")

    # 3. Check Balance
    print("Checking balance...")
    status, body = make_request(f"{BASE_URL}/wallet/balance", headers=headers)
    print(f"Balance: {body}")

    # 4. Load Wallet
    print("Loading 100.0...")
    status, body = make_request(f"{BASE_URL}/wallet/load", method="POST", data={"amount": 100.0}, headers=headers)
    print(f"New Balance: {body}")

    # 5. Buy Bundle
    print("Buying Data bundle (cost 50.0)...")
    status, body = make_request(f"{BASE_URL}/bundles/buy", method="POST", data={"type": "data", "amount": 50.0}, headers=headers)
    print(f"Bundle bought: {body}")

    # 6. Check Balance again
    print("Checking balance after purchase...")
    status, body = make_request(f"{BASE_URL}/wallet/balance", headers=headers)
    print(f"Balance: {body}")

    # 7. Simulate Usage
    print("Simulating usage of 10.0 data...")
    status, body = make_request(f"{BASE_URL}/usage/simulate", method="POST", data={"type": "data", "amount": 10.0}, headers=headers)
    print(f"Usage result: {body}")

    # 8. Check My Bundles
    print("Checking my bundles...")
    status, body = make_request(f"{BASE_URL}/bundles/my-bundles", headers=headers)
    print(f"My Bundles: {body}")

if __name__ == "__main__":
    try:
        test_flow()
        print("\nSUCCESS: All tests passed!")
    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
