import requests
from config import WATSONX_API_KEY, WATSONX_DEPLOYMENT_ID

# Cache token to avoid repeated authentication
_cached_token = None
_token_expiry = 0

def get_access_token():
    """Get or refresh IBM Cloud access token"""
    global _cached_token, _token_expiry
    import time
    
    if _cached_token and time.time() < _token_expiry:
        return _cached_token
    
    print("🔐 Getting new access token...")
    token_response = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={
            "apikey": WATSONX_API_KEY,
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
        }
    )

    if token_response.status_code != 200:
        raise Exception("Authentication failed with IBM Cloud.")

    token_data = token_response.json()
    _cached_token = token_data["access_token"]
    _token_expiry = time.time() + token_data.get("expires_in", 3600) - 300
    
    return _cached_token

def ask_agent(user_text):
    """Send user text to Watsonx Acharya (Guruji) AI Agent"""
    try:
        access_token = get_access_token()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }

        # AI Service endpoint for your Acharya agent
        url = f"https://us-south.ml.cloud.ibm.com/ml/v4/deployments/{WATSONX_DEPLOYMENT_ID}/ai_service?version=2021-05-01"
        
        # Payload in chat format for AI Agent
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": user_text
                }
            ]
        }

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            print(f"❌ API Error ({response.status_code}): {response.text[:300]}")
            return None

        data = response.json()

        # Parse AI Agent response (OpenAI-like format)
        try:
            if "choices" in data and len(data["choices"]) > 0:
                message = data["choices"][0].get("message", {})
                content = message.get("content", "")
                return content.strip()
            else:
                print("🔍 Unexpected response format:", data)
                return None
                
        except (KeyError, IndexError, TypeError) as e:
            print(f"❌ Parse error: {e}")
            return None

    except requests.Timeout:
        print("⏱️ Request timed out")
        return None
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None