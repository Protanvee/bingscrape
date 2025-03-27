from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import json
import os

app = Flask(__name__)

@app.route('/<company_name>')
def get_bing_results(company_name):
    # ... (rest of your code) ...
    try:
        # ... (fetching HTML) ...
        soup = BeautifulSoup(response.content, 'html.parser')
        results_list = soup.find('ol', {'id': 'b_results'}) # Assuming this is still correct

        if results_list:
            results_data = []
            for item in results_list.find_all('li', {'class': 'b_algo'}): # Assuming this is still correct
                # Example of updated selectors based on hypothetical HTML
                title_element = item.find('h2', {'class': 'news-card-title'})
                desc_element = item.find('span', {'class': 'article-desc'})
                link_element = title_element.find('a')['href'] if title_element and title_element.find('a') and 'href' in title_element.find('a').attrs else None
                title = title_element.get_text(strip=True) if title_element else None
                description = desc_element.get_text(strip=True) if desc_element else None

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
        return jsonify({"error": f"An unexpected error occurred: {e}"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
