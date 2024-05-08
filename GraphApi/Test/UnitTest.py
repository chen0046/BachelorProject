import sys
import os
import unittest
from aioresponses import aioresponses
import aiohttp

# Setup the path to include the directory where Optimering_2.py is located
optimize_dir = '/Users/chenxi/Desktop/Projekt/GraphApi/Optimize'
sys.path.insert(0, optimize_dir)

from Optimization import fetch,get_access_token,search_documents

class TestFetch(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Setup an aiohttp session for making HTTP requests
        self.session = aiohttp.ClientSession()

    async def asyncTearDown(self):
        # Close the session after tests are done
        await self.session.close()

    @aioresponses()
    async def test_fetch_success(self, mocked):
        # The URL here is a placeholder for testing purposes
        url = 'https://example.com/path'
        response_body = {'key': 'value'}
        # Mock the GET request to the URL with a response
        mocked.get(url, status=200, payload=response_body)
        # Call the function that needs to be tested
        response, status = await fetch(self.session, url)
        # Assert conditions to validate the function behavior
        self.assertEqual(status, 200)
        self.assertEqual(response, response_body)

class TestGetAccessToken(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.session = aiohttp.ClientSession()

    async def asyncTearDown(self):
        await self.session.close()

    @aioresponses()
    async def test_get_access_token_success(self, mocked):
        token_url = 'https://login.microsoftonline.com/08124b84-4f34-4bbe-91cc-cd51e0e0bbd9/oauth2/v2.0/token'
        response_body = {'access_token': 'mock_token'}
        mocked.post(token_url, status=200, payload=response_body)
        token = await get_access_token(self.session)
        self.assertEqual(token, 'mock_token')
        
class TestSearchDocuments(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        # Set up the session for testing
        self.session = aiohttp.ClientSession()

    async def asyncTearDown(self):
        # Clean up after tests
        await self.session.close()

    @aioresponses()
    async def test_search_documents_success(self, mocked):
        access_token = 'mock_token'
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Accept': 'application/json'
        }
        sites_url = 'https://graph.microsoft.com/v1.0/sites'
        libraries_url = 'https://graph.microsoft.com/v1.0/sites/site-123/drives'
        search_url_pattern = 'https://graph.microsoft.com/v1.0/sites/site-123/drives/library-123/root/search'

        # Mocking the API responses
        mocked.get(sites_url, status=200, payload={'value': [{'id': 'site-123'}]})
        mocked.get(libraries_url, status=200, payload={'value': [{'id': 'library-123'}]})
        for keyword in ['indberetning', 'lov', 'skema']:
            mocked.get(search_url_pattern + f"(q='{keyword}')", status=200, payload={
                'value': [{
                    'createdBy': {'user': {'displayName': 'User One'}},
                    'webUrl': 'http://link-to-doc',
                    'name': f'Document1_{keyword}'
                }]
            })

        results = await search_documents(self.session, access_token, headers)
        # Check if the results contain the correct data
        expected_results = [{
            'User': 'User One',
            'Web URL': 'http://link-to-doc',
            'Filename': f'Document1_{keyword}',
            'Keyword Used': keyword,
            'Location': 'Site: site-123, Library: library-123'
        } for keyword in ['indberetning', 'lov', 'skema']]
        
        self.assertEqual(len(results), 3)
        self.assertListEqual(results, expected_results)
        
if __name__ == '__main__':
    unittest.main()
