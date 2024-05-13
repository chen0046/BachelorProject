import asyncio
import aiohttp
import json
#in this version we have added a keyword counter
# Define Azure AD app credentials
client_id = '1aa3b689-809c-4633-84c0-89422aa83a67'
client_secret = 'pBp8Q~82oBux-P5zmIPgmbmkMlVEO~GtKDO6odh9'
tenant_id = '08124b84-4f34-4bbe-91cc-cd51e0e0bbd9'

# Define keywords to search for in documents
keywords = ['indberetning', 'lov', 'skema']

# Function to fetch data from a given URL using aiohttp
async def fetch(session, url, headers=None):
    async with session.get(url, headers=headers) as response:
        return await response.json(), response.status

# Function to retrieve access token from Microsoft Azure using client credentials flow
async def get_access_token(session):
    token_url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
    token_data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://graph.microsoft.com/.default'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    async with session.post(token_url, data=token_data, headers=headers) as response:
        res = await response.json()
        return res.get('access_token')

# Function to search for documents containing specified keywords in Microsoft Graph API
async def search_documents(session, access_token, headers):
    sites_url = 'https://graph.microsoft.com/v1.0/sites'
    results = []
    keyword_counts = {keyword: 0 for keyword in keywords}  # Initialize counts for each keyword

    sites_json, status = await fetch(session, sites_url, headers)
    if status == 200:
        for site in sites_json['value']:
            site_id = site['id']
            libraries_url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives'
            libraries_json, _ = await fetch(session, libraries_url, headers)
            for library in libraries_json['value']:
                library_id = library['id']
                for keyword in keywords:
                    search_url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{library_id}/root/search(q=\'{keyword}\')'
                    search_result, _ = await fetch(session, search_url, headers)
                    keyword_counts[keyword] += len(search_result['value'])  # Increment count for the keyword
                    for item in search_result['value']:
                        results.append({
                            'User': item.get('createdBy', {}).get('user', {}).get('displayName', 'N/A'),
                            'Web URL': item['webUrl'],
                            'Filename': item['name'],
                            'Keyword Used': keyword,
                            'Location': f"Site: {site_id}, Library: {library_id}"
                        })

    return results, keyword_counts

async def main():
    async with aiohttp.ClientSession() as session:
        access_token = await get_access_token(session)
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        results, keyword_counts = await search_documents(session, access_token, headers)
        search_data = {
            'Results': results,
            'Keyword Counts': keyword_counts
        }
        with open('search_results.json', 'w') as json_file:
            json.dump(search_data, json_file, indent=4)
        print("Search Results Saved to 'search_results.json'")

if __name__ == '__main__':
    asyncio.run(main())
