"""
Check your IBM WatsonX API quota and usage
"""
import requests
from config import WATSONX_API_KEY, WATSONX_DEPLOYMENT_ID

def get_access_token():
    """Get IBM Cloud access token"""
    token_response = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={
            "apikey": WATSONX_API_KEY,
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
        }
    )
    
    if token_response.status_code != 200:
        print("❌ Authentication failed")
        return None
    
    return token_response.json()["access_token"]

def check_deployment_status():
    """Check deployment status and details"""
    access_token = get_access_token()
    if not access_token:
        return
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json"
    }
    
    # Check deployment details
    url = f"https://us-south.ml.cloud.ibm.com/ml/v4/deployments/{WATSONX_DEPLOYMENT_ID}?version=2021-05-01"
    
    try:
        response = requests.get(url, headers=headers)
        
        print("="*70)
        print("📊 IBM WatsonX Deployment Status")
        print("="*70)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Deployment ID: {WATSONX_DEPLOYMENT_ID}")
            print(f"✅ Status: {data.get('entity', {}).get('status', {}).get('state', 'Unknown')}")
            print(f"✅ Name: {data.get('metadata', {}).get('name', 'N/A')}")
        else:
            print(f"⚠️  Status Code: {response.status_code}")
            print(f"Response: {response.text[:500]}")
        
        print("\n" + "="*70)
        print("💡 Next Steps:")
        print("="*70)
        print("1. Go to: https://cloud.ibm.com/")
        print("2. Navigate to: Resource List → AI / Machine Learning")
        print("3. Check your WatsonX service:")
        print("   - View usage/quota limits")
        print("   - Check billing status")
        print("   - Verify plan type (Lite/Pay-as-you-go)")
        print("\n4. If on Lite plan:")
        print("   ✓ 50,000 tokens/month free limit")
        print("   ✓ Resets monthly")
        print("   ✓ Consider upgrading to Pay-as-you-go")
        print("\n5. If quota exceeded:")
        print("   ✓ Wait until monthly reset")
        print("   ✓ OR upgrade your plan")
        print("   ✓ OR add payment method")
        
    except Exception as e:
        print(f"❌ Error checking deployment: {e}")

if __name__ == "__main__":
    check_deployment_status()