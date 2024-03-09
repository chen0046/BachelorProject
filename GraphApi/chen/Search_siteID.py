import requests

# Replace these with your actual values
client_id = '1aa3b689-809c-4633-84c0-89422aa83a67'
client_secret = 'pBp8Q~82oBux-P5zmIPgmbmkMlVEO~GtKDO6odh9'
tenant_id = '08124b84-4f34-4bbe-91cc-cd51e0e0bbd9'

# Get an access token
token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': 'https://graph.microsoft.com/.default'
}
token_response = requests.post(token_url, data=token_data)
access_token = token_response.json()['access_token']

# Get sites from the root
headers = {
    'Authorization': 'Bearer ' + access_token,
    'Accept': 'application/json'
}
sites_url = 'https://graph.microsoft.com/v1.0/sites'

sites_response = requests.get(sites_url, headers=headers)

# Print the display name, site ID, personal site information, and webUrl
if sites_response.status_code == 200:
    sites_result = sites_response.json()
    for item in sites_result['value']:
        site_id = item.get('id', 'N/A')
        display_name = item.get('displayName', 'N/A')
        is_personal_site = item.get('isPersonal', False)
        web_url = item.get('webUrl', 'N/A')
        print('Site ID:', site_id)
        print('Display Name:', display_name)
        print('Personal Site:', is_personal_site)
        print('Web URL:', web_url)
        print('---')
else:
    print('Request failed:', sites_response.text)