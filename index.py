from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote

app = Flask(__name__)

@app.route('/<company_name>', methods=['GET'])
def search_company(company_name):
    try:
        # Construct the Bing search URL
        query = f'site:linkedin.com "{company_name}" ("Producer" OR "Distributor")'
        encoded_query = quote(query)
        bing_url = f"https://www.bing.com/search?q={encoded_query}"
        
        # Set headers to mimic a browser request
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Make the request to Bing
        response = requests.get(bing_url, headers=headers)
        response.raise_for_status()
        
        # Parse the HTML response
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []
        
        # Find all search result items
        for item in soup.select('.b_algo'):
            title_elem = item.find('h2')
            link_elem = item.find('a')
            desc_elem = item.find('p')
            
            if title_elem and link_elem:
                result = {
                    'title': title_elem.get_text(),
                    'link': link_elem.get('href'),
                    'description': desc_elem.get_text() if desc_elem else ''
                }
                results.append(result)
        
        return jsonify({
            'company': company_name,
            'search_url': bing_url,
            'results': results,
            'count': len(results)
        })
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'message': 'An error occurred while processing your request'
        }), 500

# Required for Vercel
def handler(req, res):
    with app.app_context():
        response = app.full_dispatch_request()
        return {
            'statusCode': response.status_code,
            'body': response.get_data(as_text=True),
            'headers': dict(response.headers)
        }
