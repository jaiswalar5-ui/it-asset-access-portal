import httpx

def test_api():
    base_url = "http://127.0.0.1:8000"
    
    # Login
    response = httpx.post(f"{base_url}/auth/login", json={"email": "employee1@example.com", "password": "ChangeMe123!"})
    print("Login:", response.status_code, response.json())
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        # Get me
        response = httpx.get(f"{base_url}/auth/me", headers={"Authorization": f"Bearer {token}"})
        print("Me:", response.status_code, response.json())
        
if __name__ == "__main__":
    test_api()
