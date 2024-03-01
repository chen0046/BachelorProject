import requests
###Den finder weburl for dokumenterne
# Indtast dine klientoplysninger og autorisationsoplysninger her
client_id = '1aa3b689-809c-4633-84c0-89422aa83a67'
client_secret = 'pBp8Q~82oBux-P5zmIPgmbmkMlVEO~GtKDO6odh9'
tenant_id = '08124b84-4f34-4bbe-91cc-cd51e0e0bbd9'
site_id = 'chenalex.sharepoint.com,3a9ade75-40b3-45d0-b7d4-c9ec3b621907,3021ca16-09c3-4545-ba0f-e227b0210898'

# Få en adgangstoken
token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
token_data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': 'https://graph.microsoft.com/.default'
}
token_response = requests.post(token_url, data=token_data)
access_token = token_response.json()['access_token']

# Hent dokumenter fra SharePoint-drevet
headers = {
    'Authorization': 'Bearer ' + access_token,
    'Accept': 'application/json'
}
drive_url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drive/root/children'


drive_response = requests.get(drive_url, headers=headers)

# Udskriv svaret
if drive_response.status_code == 200:
    print(drive_response.json())
else:
    print('Forespørgslen mislykkedes:', drive_response.text)
