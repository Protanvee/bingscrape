# index.py
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import quote_plus

def get_bing_results(company_name):
    """Fetches Bing search results and extracts relevant data."""
    try:
        query = f'site:linkedin.com "{company_name}" ("Producer" OR "Distributor")'
        url = f"https://www.bing.com/search?pglt=299&q={quote_plus(query)}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        soup = BeautifulSoup(response.content, "html.parser")
        results = []
        for item in soup.select("#b_results > li.b_algo"):
            title_element = item.select_one("h2 a")
            description_element = item.select_one("p.b_lineclamp2")
            link_element = item.select_one("h2 a")
            if title_element and description_element and link_element:
                title = title_element.text.strip()
                description = description_element.text.strip()
                link = link_element["href"]
                results.append({"title": title, "description": description, "link": link})

        return results
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}

def handler(event, context):
    """Vercel handler function."""
    path = event["path"]
    if path.startswith("/"):
        company_name = path[1:]
        results = get_bing_results(company_name)
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(results),
        }
    else:
        return {"statusCode": 404, "body": "Not Found"}
