import json
import requests
import time

# Azure AD app credentials
client_id = '1aa3b689-809c-4633-84c0-89422aa83a67'
client_secret = 'pBp8Q~82oBux-P5zmIPgmbmkMlVEO~GtKDO6odh9'
tenant_id = '08124b84-4f34-4bbe-91cc-cd51e0e0bbd9'

# Function to authenticate and get access token
def get_access_token():
    token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default',
        'grant_type': 'client_credentials'
    }
    response = requests.post(token_url, data=payload)
    return response.json().get('access_token')

# Function to search for files in OneDrive of a user
def search_user_onedrive(access_token, user_id, keywords):
    files_found = []
    for keyword in keywords:
        drive_url = f"https://graph.microsoft.com/v1.0/users/{user_id}/drive/root/search(q='{keyword}')"
        headers = {'Authorization': 'Bearer ' + access_token}
        response = requests.get(drive_url, headers=headers)
        files = response.json().get('value', [])
        for file in files:
            files_found.append({
                'user': user_map.get(user_id, 'Unknown'),
                'web_url': file.get('webUrl'),
                'file_name': file.get('name'),
                'keyword': keyword
            })
    return files_found

# Get access token
access_token = get_access_token()

# Get list of users in organization
users_url = "https://graph.microsoft.com/v1.0/users"
headers = {'Authorization': 'Bearer ' + access_token}
response = requests.get(users_url, headers=headers)
users_data = response.json().get('value', [])

# User ID to user name mapping
user_map = {user.get('id'): user.get('displayName') for user in users_data}

# Keywords to search for
keywords = ["onedrive"]

# Dictionary to store search results by user
search_results = {}

# Loop 10 times
total_time = 0
for i in range(1, 11):
    start_time = time.time()

    # Search for files in OneDrive of each user
    for user in users_data:
        user_id = user.get('id')
        user_name = user.get('displayName')
        files = search_user_onedrive(access_token, user_id, keywords)
        search_results[user_name] = files

    end_time = time.time()
    iteration_time = end_time - start_time
    total_time += iteration_time
    print(f"Iteration {i} execution time: {iteration_time} seconds")

# Write search results to a JSON file
with open('onedrive_search_results.json', 'w') as f:
    json.dump(search_results, f, indent=4)

average_time = total_time / 10
print("Average execution time:", average_time, "seconds")
