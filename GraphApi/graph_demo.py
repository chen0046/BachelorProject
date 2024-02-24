import json

import requests
from msal import ConfidentialClientApplication

client_id = 'f03fc567-f4ca-4441-ba9b-7722847749de'
client_secret = 'q.p8Q~lmZG.vffhH9VotMtQxruZxU.9JhiRVZcRa'
tenant_id = 'dcd7015c-e0eb-4ef6-8ce5-499102a2c4e1'

msal_authority = f"https://login.microsoftonline.com/{tenant_id}"

msal_scope = ["https://graph.microsoft.com/.default"]

msal_app = ConfidentialClientApplication(
    client_id=client_id,
    client_credential=client_secret,
    authority=msal_authority,
)

result = msal_app.acquire_token_silent(
    scopes=msal_scope,
    account=None,
)

if not result:
    result = msal_app.acquire_token_for_client(scopes=msal_scope)

if "access_token" in result:
    access_token = result["access_token"]
else:
    raise Exception("No Access Token found")

headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
}

response = requests.get(
    url="https://graph.microsoft.com/v1.0/users",
    headers=headers,
)

print(json.dumps(response.json(), indent=4))
