from fastapi import FastAPI, HTTPException
from playwright.sync_api import sync_playwright

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Bing Scraper API is running!"}

@app.get("/search/{company}")
def search(company: str):
    search_url = f"https://www.bing.com/search?q=site%3Alinkedin.com+{company}+(Producer+OR+Distributor)"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(search_url, timeout=60000)

        results = []
        search_results = page.query_selector_all("ol#b_results li.b_algo")

        if not search_results:
            browser.close()
            raise HTTPException(status_code=404, detail="No results found")

        for result in search_results:
            title_element = result.query_selector("h2 a")
            description_element = result.query_selector("p")

            title = title_element.inner_text() if title_element else "No title"
            link = title_element.get_attribute("href") if title_element else "No link"
            description = description_element.inner_text() if description_element else "No description"

            results.append({"title": title, "link": link, "description": description})

        browser.close()
        return {"results": results}
