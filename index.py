from fastapi import FastAPI
from playwright.sync_api import sync_playwright
from typing import Dict, List

app = FastAPI()

def fetch_bing_results(query: str) -> List[Dict]:
    search_url = f"https://www.bing.com/search?q=site%3Alinkedin.com+%22{query}%22+(%22Producer%22+OR+%22Distributor%22)"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(search_url, timeout=60000)

        results = []
        items = page.query_selector_all("#b_results .b_algo")

        for item in items:
            title_element = item.query_selector("h2 a")
            desc_element = item.query_selector("p")

            if title_element:
                results.append({
                    "title": title_element.inner_text(),
                    "description": desc_element.inner_text() if desc_element else "",
                    "url": title_element.get_attribute("href")
                })

        browser.close()
    return results

@app.get("/")
def home():
    return {"message": "Use /search/{company_name} to fetch Bing results."}

@app.get("/search/{company_name}")
def search(company_name: str):
    results = fetch_bing_results(company_name)
    return {"company": company_name, "results": results}
