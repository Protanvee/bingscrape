from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
from typing import Dict, List

app = FastAPI()

def fetch_bing_results(query: str) -> List[Dict]:
    url = f"https://www.bing.com/search?q=site%3Alinkedin.com+%22{query}%22+(%22Producer%22+OR+%22Distributor%22)"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    results = []
    for item in soup.select("#b_results .b_algo"):
        title_element = item.find("h2")
        desc_element = item.find("p")
        link_element = title_element.find("a") if title_element else None

        if title_element and link_element:
            results.append({
                "title": title_element.get_text(),
                "description": desc_element.get_text() if desc_element else "",
                "url": link_element["href"]
            })

    return results

@app.get("/")
def home():
    return {"message": "Use /search/company_name to fetch Bing results."}

@app.get("/search/{company_name}")
def search(company_name: str):
    results = fetch_bing_results(company_name)
    return {"company": company_name, "results": results}
