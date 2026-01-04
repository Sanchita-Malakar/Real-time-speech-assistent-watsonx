"""
Test AI Agent endpoints for Acharya deployment
"""
import requests
from config import WATSONX_API_KEY, WATSONX_DEPLOYMENT_ID, WATSONX_SPACE_ID

def get_token():
    response = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={
            "apikey": WATSONX_API_KEY,
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
        }
    )
    return response.json()["access_token"]

def test_agent_endpoints():
    print("🔐 Getting token...")
    token = get_token()
    print("✅ Token received\n")
    
    print(f"📦 Testing AI Agent deployment: {WATSONX_DEPLOYMENT_ID}")
    print(f"📦 In space: {WATSONX_SPACE_ID}\n")
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    # Test 1: AI Service endpoint (for agents)
    print("="*60)
    print("Test 1: AI Service Endpoint")
    print("="*60)
    
    url1 = f"https://us-south.ml.cloud.ibm.com/ml/v4/deployments/{WATSONX_DEPLOYMENT_ID}/ai_service?version=2021-05-01"
    payload1 = {
        "messages": [
            {"role": "user", "content": "Hello, how are you?"}
        ]
    }
    
    try:
        response = requests.post(url1, headers=headers, json=payload1, timeout=15)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ SUCCESS! This is an AI Agent deployment")
            print("Response:", response.json())
            return "ai_service", url1, payload1
        else:
            print(f"Response: {response.text[:400]}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Predictions endpoint for agents
    print("\n" + "="*60)
    print("Test 2: Predictions Endpoint (AI Agent)")
    print("="*60)
    
    url2 = f"https://us-south.ml.cloud.ibm.com/ml/v4/deployments/{WATSONX_DEPLOYMENT_ID}/predictions?version=2021-05-01"
    payload2 = {
        "input_data": [{
            "values": [
                {
                    "messages": [
                        {"role": "user", "content": "Hello, how are you?"}
                    ]
                }
            ]
        }]
    }
    
    try:
        response = requests.post(url2, headers=headers, json=payload2, timeout=15)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ SUCCESS! This format works")
            print("Response:", response.json())
            return "predictions", url2, payload2
        else:
            print(f"Response: {response.text[:400]}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Get deployment details
    print("\n" + "="*60)
    print("Test 3: Get Deployment Details")
    print("="*60)
    
    url3 = f"https://us-south.ml.cloud.ibm.com/ml/v4/deployments/{WATSONX_DEPLOYMENT_ID}?version=2021-05-01&space_id={WATSONX_SPACE_ID}"
    
    try:
        response = requests.get(url3, headers=headers, timeout=15)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("\n📋 Deployment Information:")
            print(f"Name: {data.get('metadata', {}).get('name', 'N/A')}")
            print(f"Status: {data.get('entity', {}).get('status', {}).get('state', 'N/A')}")
            
            # Check asset type
            asset = data.get('entity', {}).get('asset', {})
            print(f"Asset ID: {asset.get('id', 'N/A')}")
            
            # Check if it's a foundation model or custom
            if 'custom' in data.get('entity', {}):
                print("Type: Custom deployment")
            
            # Print full entity structure
            print("\n🔍 Full entity structure:")
            import json
            print(json.dumps(data.get('entity', {}), indent=2))
            
        else:
            print(f"Response: {response.text[:400]}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 4: Direct inference endpoint
    print("\n" + "="*60)
    print("Test 4: Direct Inference")
    print("="*60)
    
    url4 = f"https://us-south.ml.cloud.ibm.com/ml/v4/deployments/{WATSONX_DEPLOYMENT_ID}/predictions?version=2021-05-01"
    payload4 = {
        "input": "Hello, how are you?"
    }
    
    try:
        response = requests.post(url4, headers=headers, json=payload4, timeout=15)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ SUCCESS!")
            print("Response:", response.json())
            return "simple_predictions", url4, payload4
        else:
            print(f"Response: {response.text[:400]}")
    except Exception as e:
        print(f"Error: {e}")
    
    return None, None, None

if __name__ == "__main__":
    endpoint_type, url, payload = test_agent_endpoints()
    
    if endpoint_type:
        print("\n" + "="*60)
        print("✅ WORKING CONFIGURATION FOUND!")
        print("="*60)
        print(f"Endpoint Type: {endpoint_type}")
        print(f"URL: {url}")
        print(f"Payload format: {payload}")
    else:
        print("\n" + "="*60)
        print("❌ No working endpoint found")
        print("="*60)
        print("Please check your deployment in Watsonx.ai console")
        print("Go to: Deployments > Acharya > View details")
        print("Check what type of deployment it is (Model/Agent/Custom)")
        