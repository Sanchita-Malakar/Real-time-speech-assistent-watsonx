"""
Test the Acharya deployment directly
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

def test_deployment():
    print("🔐 Getting token...")
    token = get_token()
    print("✅ Token received")
    
    print(f"\n📦 Testing deployment: {WATSONX_DEPLOYMENT_ID}")
    print(f"📦 In space: {WATSONX_SPACE_ID}")
    
    # Test different endpoint formats
    endpoints = [
        # Format 1: Standard generation endpoint
        {
            "name": "Generation endpoint",
            "url": f"https://us-south.ml.cloud.ibm.com/ml/v1/deployments/{WATSONX_DEPLOYMENT_ID}/generation/text?version=2023-05-29",
            "payload": {
                "input": "Hello, how are you?",
                "parameters": {
                    "max_new_tokens": 50,
                    "decoding_method": "greedy"
                }
            }
        },
        # Format 2: Text chat endpoint
        {
            "name": "Text chat endpoint",
            "url": f"https://us-south.ml.cloud.ibm.com/ml/v1/deployments/{WATSONX_DEPLOYMENT_ID}/text/chat?version=2023-05-29",
            "payload": {
                "messages": [
                    {"role": "user", "content": "Hello, how are you?"}
                ],
                "max_tokens": 50
            }
        },
        # Format 3: With space_id parameter
        {
            "name": "Generation with space_id",
            "url": f"https://us-south.ml.cloud.ibm.com/ml/v1/deployments/{WATSONX_DEPLOYMENT_ID}/generation/text?version=2023-05-29&space_id={WATSONX_SPACE_ID}",
            "payload": {
                "input": "Hello, how are you?",
                "parameters": {
                    "max_new_tokens": 50,
                    "decoding_method": "greedy"
                }
            }
        }
    ]
    
    for endpoint in endpoints:
        print("\n" + "="*60)
        print(f"Testing: {endpoint['name']}")
        print("="*60)
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        try:
            response = requests.post(
                endpoint["url"],
                headers=headers,
                json=endpoint["payload"],
                timeout=15
            )
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ SUCCESS!")
                data = response.json()
                print("Response:", data)
                
                # Try to extract text
                if "results" in data:
                    text = data["results"][0].get("generated_text", "")
                    print(f"\n💬 Generated: {text}")
                elif "choices" in data:
                    text = data["choices"][0]["message"]["content"]
                    print(f"\n💬 Generated: {text}")
                    
                print("\n✅ This format works! Use this in agent.py")
                return True
            else:
                print(f"❌ Failed")
                print(f"Response: {response.text[:300]}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    return False

if __name__ == "__main__":
    test_deployment()