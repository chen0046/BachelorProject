import requests
from msal import ConfidentialClientApplication
import json

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
result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
access_token = result['access_token']

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
                "site_id": site_id
            }
            files_info.append(file_info)

    return files_info

# List to store file information
all_files_info = []

# Search for files containing each keyword and collect information
for keyword in keywords:
    files_info = search_files_and_collect_info(keyword, access_token)
    all_files_info.extend(files_info)

# Write file information to a JSON file
with open("files_info.json", "w") as json_file:
    json.dump(all_files_info, json_file, indent=4)

print("File information saved to files_info.json.")
