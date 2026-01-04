"""
This script will help you find your Watsonx projects, spaces, and deployments
"""
import requests
from config import WATSONX_API_KEY

def get_token():
    response = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={
            "apikey": WATSONX_API_KEY,
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey"
        }
    )
    return response.json()["access_token"]

def list_projects(token):
    """List all Watsonx projects"""
    print("\n" + "="*60)
    print("📁 YOUR WATSONX PROJECTS:")
    print("="*60)
    
    url = "https://api.dataplatform.cloud.ibm.com/v2/projects"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if "resources" in data and len(data["resources"]) > 0:
                for project in data["resources"]:
                    print(f"\n✅ Project Name: {project.get('entity', {}).get('name', 'N/A')}")
                    print(f"   Project ID: {project.get('metadata', {}).get('guid', 'N/A')}")
                return data["resources"]
            else:
                print("No projects found")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")
    return []

def list_spaces(token):
    """List all deployment spaces"""
    print("\n" + "="*60)
    print("🚀 YOUR DEPLOYMENT SPACES:")
    print("="*60)
    
    url = "https://api.dataplatform.cloud.ibm.com/v2/spaces"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if "resources" in data and len(data["resources"]) > 0:
                for space in data["resources"]:
                    print(f"\n✅ Space Name: {space.get('entity', {}).get('name', 'N/A')}")
                    print(f"   Space ID: {space.get('metadata', {}).get('id', 'N/A')}")
                return data["resources"]
            else:
                print("No deployment spaces found")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error: {e}")
    return []

def list_deployments(token, space_id):
    """List deployments in a space"""
    print(f"\n📦 Deployments in space {space_id}:")
    
    url = f"https://us-south.ml.cloud.ibm.com/ml/v4/deployments?space_id={space_id}&version=2021-05-01"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if "resources" in data and len(data["resources"]) > 0:
                for deployment in data["resources"]:
                    metadata = deployment.get('metadata', {})
                    entity = deployment.get('entity', {})
                    print(f"\n   ✅ Deployment Name: {metadata.get('name', 'N/A')}")
                    print(f"      Deployment ID: {metadata.get('id', 'N/A')}")
                    print(f"      Status: {entity.get('status', {}).get('state', 'N/A')}")
            else:
                print("   No deployments found in this space")
        else:
            print(f"   Error: {response.status_code}")
    except Exception as e:
        print(f"   Error: {e}")

def test_with_project_id(token, project_id):
    """Test using project ID for prompt lab"""
    print(f"\n🧪 Testing Prompt Lab with Project ID: {project_id}")
    
    url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    payload = {
        "model_id": "ibm/granite-13b-chat-v2",
        "input": "Hello, how are you?",
        "parameters": {
            "max_new_tokens": 50,
            "decoding_method": "greedy"
        },
        "project_id": project_id
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS! Response:")
            print(data.get("results", [{}])[0].get("generated_text", ""))
            return True
        else:
            print(f"Response: {response.text[:300]}")
    except Exception as e:
        print(f"Error: {e}")
    return False

if __name__ == "__main__":
    print("🔐 Getting access token...")
    token = get_token()
    print("✅ Token received\n")
    
    # List all resources
    projects = list_projects(token)
    spaces = list_spaces(token)
    
    # List deployments in each space
    if spaces:
        for space in spaces:
            space_id = space.get('metadata', {}).get('id')
            if space_id:
                list_deployments(token, space_id)
    
    # Try using the first project for Prompt Lab
    if projects:
        print("\n" + "="*60)
        print("💡 TESTING PROJECT-BASED GENERATION (Prompt Lab)")
        print("="*60)
        first_project_id = projects[0].get('metadata', {}).get('guid')
        if first_project_id:
            success = test_with_project_id(token, first_project_id)
            if success:
                print("\n" + "="*60)
                print("✅ RECOMMENDED CONFIGURATION:")
                print("="*60)
                print(f"Use this in your config.py:")
                print(f'WATSONX_PROJECT_ID = "{first_project_id}"')
                print('WATSONX_URL = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"')
    
    print("\n" + "="*60)
    print("📋 NEXT STEPS:")
    print("="*60)
    print("1. Copy the Project ID or Deployment ID from above")
    print("2. Update your config.py with the correct ID")
    print("3. If using Project ID, you'll use Prompt Lab mode")
    print("4. If using Deployment ID, you'll use deployment mode")