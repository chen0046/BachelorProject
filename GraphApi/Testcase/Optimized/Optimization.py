import asyncio
import aiohttp
import json
import time

client_id = '1aa3b689-809c-4633-84c0-89422aa83a67'
client_secret = 'pBp8Q~82oBux-P5zmIPgmbmkMlVEO~GtKDO6odh9'
tenant_id = '08124b84-4f34-4bbe-91cc-cd51e0e0bbd9'
keywords = ['Bog', 'Flaske', "Mus"]

async def fetch(session, url, headers=None):
    async with session.get(url, headers=headers) as response:
        return await response.json(), response.status

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

async def search_documents(session, access_token, headers):
    sites_url = 'https://graph.microsoft.com/v1.0/sites'
    results = []
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
                    for item in search_result['value']:
                        results.append({
                            'User': item.get('createdBy', {}).get('user', {}).get('displayName', 'N/A'),
                            'Web URL': item['webUrl'],
                            'Filename': item['name'],
                            'Keyword Used': keyword,
                            'Location': f"Site: {site_id}, Library: {library_id}"
                        })
    return results

async def main():
    times = []
    for i in range(10):
        start_time = time.time()
        async with aiohttp.ClientSession() as session:
            access_token = await get_access_token(session)
            headers = {
                'Authorization': f'Bearer {access_token}',
                'Accept': 'application/json'
            }
            results = await search_documents(session, access_token, headers)
            with open(f'search_results_{i}.json', 'w') as json_file:
                json.dump(results, json_file, indent=4)
        end_time = time.time()
        elapsed_time = end_time - start_time
        times.append(elapsed_time)
        print(f'Iteration {i+1} execution time: {elapsed_time:.6f} seconds')
    
    average_time = sum(times) / len(times)
    print(f'Average execution time: {average_time:.6f} seconds')

if __name__ == '__main__':
    asyncio.run(main())
