from flask import Flask, jsonify
import requests

app = Flask(__name__)

@app.route('/<company_name>', methods=['GET'])
def get_bing_search_results(company_name):
    # Construct the Bing search URL
    bing_search_url = f"https://www.bing.com/search?pglt=299&q=site%3A+linkedin.com%20%22{company_name}%22%20(%22Producer%22%20OR%20%22Distributor%22)"

    # Make the API request to Bing
    response = requests.get(bing_search_url)

    # Parse the HTML response and extract the relevant information
    html_content = response.text
    start_index = html_content.find('<ol id="b_results" class="">')
    end_index = html_content.find('</ol>') + len('</ol>')
    search_results_html = html_content[start_index:end_index]

    # Extract the title, description, and summary excerpt from the search results
    search_results = []
    for result in search_results_html.split('<li class="b_algo"'):
        if 'b_tpcn' in result:
            title = result.split('<div class="tptt">')[1].split('</div>')[0]
            description = result.split('<p class="b_lineclamp2">')[1].split('</p>')[0]
            summary_excerpt = description.split(' ... ')[0]
            search_results.append({
                'title': title,
                'description': description,
                'summary_excerpt': summary_excerpt
            })

    return jsonify(search_results)

if __name__ == '__main__':
    app.run()
