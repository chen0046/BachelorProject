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

# Function to get site owner's email
def get_site_owner_email(site_id, access_token):
    headers = {
        'Authorization': 'Bearer ' + access_token,
        'Content-Type': 'application/json'
    }
    site_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}"
    response = requests.get(site_url, headers=headers)
    site_info = response.json()
    owner_email = None
    if 'siteCollection' in site_info and 'owner' in site_info['siteCollection']:
        owner = site_info['siteCollection']['owner']
        owner_id = owner.get('user', {}).get('id')
        if owner_id:
            owner_info_url = f"https://graph.microsoft.com/v1.0/users/{owner_id}"
            owner_response = requests.get(owner_info_url, headers=headers)
            owner_info = owner_response.json()
            if 'mail' in owner_info:
                owner_email = owner_info['mail']
    return owner_email

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
        site_owner_email = get_site_owner_email(site_id, access_token)
        files_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root/search(q='{keyword}')"
        response = requests.get(files_url, headers=headers)
        files = response.json()['value']
        for file in files:
            file_info = {
                "keyword": keyword,
                "file_name": file['name'],
                "file_url": file['webUrl'],
                "site_id": site_id,
                "site_owner_email": site_owner_email,  # Add site owner's email
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
            if 'createdBy' in file:
                creator = file['createdBy']
                creator_info_url = creator.get('user', {}).get('@odata.id')
                if creator_info_url:
                    creator_response = requests.get(creator_info_url, headers=headers)
                    creator_info = creator_response.json()
                    if 'mail' in creator_info:
                        file_info["owner_email"] = creator_info['mail']
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

# Print file information and users with access
for file_info in all_files_info:
    print(f"File Name: {file_info['file_name']}")
    print(f"File URL: {file_info['file_url']}")
    print(f"Owner's Email: {file_info['owner_email']}")
    print(f"Site Owner's Email: {file_info['site_owner_email']}")
    print(f"Users with Access: {', '.join(file_info['users_with_access'])}\n")

print("File information saved to files_info.json.")
