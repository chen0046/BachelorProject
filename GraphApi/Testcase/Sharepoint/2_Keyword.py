import requests
from msal import ConfidentialClientApplication
import json
import time

# Azure AD app credentials
client_id = '1aa3b689-809c-4633-84c0-89422aa83a67'
client_secret = 'pBp8Q~82oBux-P5zmIPgmbmkMlVEO~GtKDO6odh9'
tenant_id = '08124b84-4f34-4bbe-91cc-cd51e0e0bbd9'

# Authenticate with Azure AD
authority = f"https://login.microsoftonline.com/{tenant_id}"
app = ConfidentialClientApplication(
    client_id,
    authority=authority,
    client_credential=client_secret
)

# Keywords to search for
keywords = ["minsite", "dinsite"]

# Function to search for files and collect information
def search_files_and_collect_info(keyword, access_token):
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    search_url = f"https://graph.microsoft.com/v1.0/sites?search=*"
    response = requests.get(search_url, headers=headers)
    sites = response.json()['value']

    files_info = []

    for site in sites:
        site_id = site['id']
        files_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root/search(q='{keyword}')"
        response = requests.get(files_url, headers=headers)
        files = response.json()['value']
        for file in files:
            file_info = {
                "keyword": keyword,
                "file_name": file['name'],
                "file_url": file['webUrl'],
                "site_id": site_id,
                "users_with_access": [],  # Initialize list to store users with access
                "owner_email": None  # Initialize owner's email
            }
            # Check sharing status and get users with access
            sharing_info_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/items/{file['id']}/permissions"
            sharing_response = requests.get(sharing_info_url, headers=headers)
            sharing_info = sharing_response.json().get('value', [])  # Use .get() to handle missing 'value'
            for permission in sharing_info:
                if 'grantedTo' in permission:
                    granted_to = permission['grantedTo']
                    if 'user' in granted_to:
                        user = granted_to['user']
                        if 'email' in user:
                            file_info["users_with_access"].append(user['email'])
            # Get owner's email
            if 'createdBy' in file and 'user' in file['createdBy'] and 'email' in file['createdBy']['user']:
                file_info["owner_email"] = file['createdBy']['user']['email']
            files_info.append(file_info)

    return files_info

# List to store file information
all_files_info = []

# Loop to run the code 10 times and measure time
total_execution_time = 0
for i in range(10):
    start_time = time.time()
    
    # Authenticate with Azure AD
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    access_token = result['access_token']
    
    # Search for files containing each keyword and collect information
    for keyword in keywords:
        files_info = search_files_and_collect_info(keyword, access_token)
        all_files_info.extend(files_info)


    execution_time = time.time() - start_time
    total_execution_time += execution_time
    print(f"Iteration {i+1} execution time: {execution_time} seconds")

# Calculate and print average execution time
average_execution_time = total_execution_time / 10
print(f"Average execution time: {average_execution_time} seconds")
