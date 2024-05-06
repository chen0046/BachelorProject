import requests
from msal import ConfidentialClientApplication

# Microsoft Graph API endpoint for searching files in SharePoint sites
search_url = "https://graph.microsoft.com/v1.0/sites?search=*"

# Azure AD app credentials
client_id = '1aa3b689-809c-4633-84c0-89422aa83a67'
client_secret = 'pBp8Q~82oBux-P5zmIPgmbmkMlVEO~GtKDO6odh9'
tenant_id = '08124b84-4f34-4bbe-91cc-cd51e0e0bbd9'

# Authenticate with the Graph API
authority = f"https://login.microsoftonline.com/{tenant_id}"
app = ConfidentialClientApplication(
    client_id,
    authority=authority,
    client_credential=client_secret
)
result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
access_token = result['access_token']

# Function to search for keyword in file content
def search_file(keyword, file_content):
    return keyword.lower() in file_content.lower()

# Keyword to search for
keyword = "dog"

# Headers for Graph API requests
headers = {
    'Authorization': 'Bearer ' + access_token,
    'Content-Type': 'application/json'
}

# Search for SharePoint sites
response = requests.get(search_url, headers=headers)
sites = response.json()['value']

# Iterate over all sites and search for files containing the keyword
for site in sites:
    site_id = site['id']
    files_url = f"https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root/search(q='{keyword}')"
    response = requests.get(files_url, headers=headers)
    files = response.json()['value']
    for file in files:
        print(f"Keyword found in file: {file['name']}")
        print(f"File URL: {file['webUrl']}")
