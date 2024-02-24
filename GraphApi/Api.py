from msal import ConfidentialClientApplication
import requests

client_id = 'f03fc567-f4ca-4441-ba9b-7722847749de'
client_secret = 'q.p8Q~lmZG.vffhH9VotMtQxruZxU.9JhiRVZcRa'
tenant_id = 'dcd7015c-e0eb-4ef6-8ce5-499102a2c4e1'

msal_authourity= f'https://login.microsoftonline.com/{tenant_id}'
msal_scope = ['https://graph.microsoft.com/.default']


