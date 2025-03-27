from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import json
import os

app = Flask(__name__)

@app.route('/<company_name>')
def get_bing_results(company_name):
    """
    Fetches Bing search results for a given company name and returns them as JSON.
    """
    search_query = f'site:linkedin.com "{company_name}" ("Producer" OR "Distributor")'
    bing_url = f'https://www.bing.com/search?q={search_query.replace(" ", "+")}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    try:
        response = requests.get(bing_url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        # Print the HTML content to the logs for debugging
        print("Fetched HTML Content:")
        print(response.text)

        soup = BeautifulSoup(response.content, 'html.parser')
        results_list = soup.find('ol', {'id': 'b_results'})

        if results_list:
            results_data = []
            for item in results_list.find_all('li', {'class': 'b_algo'}):
                title_element = item.find('a', {'class': 'tilk'})
                desc_element = item.find('p', {'class': 'b_lineclamp2'})
                if not desc_element:
                    desc_element = item.find('p', {'class': 'b_lineclamp3'})
                if not desc_element:
                    desc_element = item.find('div', {'class': 'b_imgcap_altitle'}).find_next('p') if item.find('div', {'class': 'b_imgcap_altitle'}) else None

                link_element = title_element['href'] if title_element and 'href' in title_element.attrs else None
                title = title_element.get_text() if title_element else None
                description = desc_element.get_text() if desc_element else None

                results_data.append({
                    'title': title,
                    'description': description,
                    'link': link_element
                })
            return jsonify(results_data)
        else:
            return jsonify({"error": "No search results found."})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Error fetching Bing search results: {e}"})
    except Exception as e:
        # The 'response' variable might not be defined here if requests.get() failed
        return jsonify({"error": f"An unexpected error occurred: {e}"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
