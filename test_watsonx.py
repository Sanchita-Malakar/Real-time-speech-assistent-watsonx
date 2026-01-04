"""
Run this script to test different Watsonx payload formats
and find which one works with your deployment
"""
import requests
from config import WATSONX_API_KEY, WATSONX_DEPLOYMENT_ID

def get_token():
    response = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={
            "apikey": WATSONX_API_KEY,
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
        }
    )
    return response.json()["access_token"]

def test_format_1(token):
    """Test AI Service chat format"""
    print("\n" + "="*60)
    print("Testing Format 1: AI Service Chat")
    print("="*60)
    
    url = f"https://us-south.ml.cloud.ibm.com/ml/v1/deployments/{WATSONX_DEPLOYMENT_ID}/generation/text?version=2023-05-29"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "input": "Hello, how are you?",
        "parameters": {
            "max_new_tokens": 100
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_format_2(token):
    """Test prediction format"""
    print("\n" + "="*60)
    print("Testing Format 2: Predictions")
    print("="*60)
    
    url = f"https://us-south.ml.cloud.ibm.com/ml/v4/deployments/{WATSONX_DEPLOYMENT_ID}/predictions?version=2021-05-01"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "input_data": [{
            "values": [["Hello, how are you?"]]
        }]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_format_3(token):
    """Test text generation format"""
    print("\n" + "="*60)
    print("Testing Format 3: Text Generation")
    print("="*60)
    
    url = f"https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "model_id": "ibm/granite-13b-chat-v2",  # Try common model
        "input": "Hello, how are you?",
        "parameters": {
            "max_new_tokens": 100,
            "decoding_method": "greedy"
        },
        "project_id": WATSONX_DEPLOYMENT_ID  # Sometimes it's project_id
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text[:500]}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    print("🔐 Getting access token...")
    token = get_token()
    print("✅ Token received")
    
    # Test all formats
    results = {
        "Format 1 (AI Service)": test_format_1(token),
        "Format 2 (Predictions)": test_format_2(token),
        "Format 3 (Text Gen)": test_format_3(token)
    }
    
    print("\n" + "="*60)
    print("RESULTS:")
    print("="*60)
    for name, success in results.items():
        status = "✅ WORKS" if success else "❌ Failed"
        print(f"{name}: {status}")
    
    print("\nℹ️ Use the working format in your agent.py file")