import requests
import json
import concurrent.futures

# Credentials and tenant details
client_id = '1aa3b689-809c-4633-84c0-89422aa83a67'
client_secret = 'pBp8Q~82oBux-P5zmIPgmbmkMlVEO~GtKDO6odh9'
tenant_id = '08124b84-4f34-4bbe-91cc-cd51e0e0bbd9'

# Keywords to search
keywords = ['Mus', 'Bog', "Flaske"]

# Function to get access token
def get_access_token():
    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }
    response = requests.post(token_url, data=token_data)
    return response.json().get('access_token')

# Function to make API requests
def make_request(url, headers):
    response = requests.get(url, headers=headers)
    return response.json()

# Function to search within a library
def search_in_library(site_id, library_id, headers):
    local_results = []
    for keyword in keywords:
        search_url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{library_id}/root/search(q=\'{keyword}\')'
        search_response = requests.get(search_url, headers=headers)
        if search_response.status_code == 200:
            search_result = search_response.json()
            for item in search_result['value']:
                document_name = item.get('name', 'N/A')
                web_url = item.get('webUrl', 'N/A')
                user = item.get('createdBy', {}).get('user', {}).get('displayName', 'N/A')
                location = f"Site: {site_id}, Library: {library_id}"
                local_results.append({
                    'User': user,
                    'Web URL': web_url,
                    'Filename': document_name,
                    'Keyword Used': keyword,
                    'Location': location
                })
    return local_results

# Main execution logic
access_token = get_access_token()
headers = {
    'Authorization': 'Bearer ' + access_token,
    'Accept': 'application/json'
}
sites_url = 'https://graph.microsoft.com/v1.0/sites'
sites_result = make_request(sites_url, headers)

results = []
with concurrent.futures.ThreadPoolExecutor() as executor:
    future_to_library = {}
    for item in sites_result.get('value', []):
        site_id = item.get('id', 'N/A')
        libraries_url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives'
        libraries_result = make_request(libraries_url, headers)
        for library in libraries_result.get('value', []):
            library_id = library.get('id', 'N/A')
            future = executor.submit(search_in_library, site_id, library_id, headers)
            future_to_library[future] = (site_id, library_id)

    for future in concurrent.futures.as_completed(future_to_library):
        results.extend(future.result())

# Write results to a JSON file
with open('search_results.json', 'w') as json_file:
    json.dump(results, json_file, indent=4)
