import requests
import json

# Replace these with your actual values
client_id = '1aa3b689-809c-4633-84c0-89422aa83a67'
client_secret = 'pBp8Q~82oBux-P5zmIPgmbmkMlVEO~GtKDO6odh9'
tenant_id = '08124b84-4f34-4bbe-91cc-cd51e0e0bbd9'

# Define the keyword
keyword = 'minsite'

# Get an access token
token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': 'https://graph.microsoft.com/.default'
}
token_response = requests.post(token_url, data=token_data)
access_token = token_response.json().get('access_token')

# Get sites from the root
headers = {
    'Authorization': 'Bearer ' + access_token,
    'Accept': 'application/json'
}
sites_url = 'https://graph.microsoft.com/v1.0/sites'

sites_response = requests.get(sites_url, headers=headers)

# Create a list to store results
results = []

# Print the display name, site ID, personal site information, and webUrl
if sites_response.status_code == 200:
    sites_result = sites_response.json()
    for item in sites_result['value']:
        site_id = item.get('id', 'N/A')

        # Get document libraries in the site
        libraries_url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives'
        libraries_response = requests.get(libraries_url, headers=headers)

        if libraries_response.status_code == 200:
            libraries_result = libraries_response.json()
            for library in libraries_result['value']:
                library_id = library.get('id', 'N/A')

                # Search for documents with the keyword in the library
                search_url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{library_id}/root/search(q=\'{keyword}\')'
                search_response = requests.get(search_url, headers=headers)

                if search_response.status_code == 200:
                    search_result = search_response.json()
                    for item in search_result['value']:
                        document_name = item.get('name', 'N/A')
                        download_url = item.get('@microsoft.graph.downloadUrl', 'N/A')
                        user = item.get('createdBy', {}).get('user', {}).get('displayName', 'N/A')
                        web_url = item.get('webUrl', 'N/A')
                        location = f"Site: {site_id}, Library: {library_id}"

                        if download_url == 'N/A':
                            results.append({
                                'User': user,
                                'Web URL': web_url,
                                'Filename': document_name,
                                'Keyword Used': keyword,
                                'Location': location
                            })
                        else:
                            results.append({
                                'User': user,
                                'Web URL': web_url,
                                'Filename': document_name,
                                'Keyword Used': keyword,
                                'Location': location
                            })

                else:
                    print('Search request failed:', search_response.text)

        else:
            print('Get libraries request failed:', libraries_response.text)

else:
    print('Request failed:', sites_response.text)

# Write results to a JSON file
with open('search_results.json', 'w') as json_file:
    json.dump(results, json_file, indent=4)