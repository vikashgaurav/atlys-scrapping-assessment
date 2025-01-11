from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional
import requests
from bs4 import BeautifulSoup
import json
import os

app = FastAPI()

# Pydantic model to define input settings
class ScrapeSettings(BaseModel):
    limit_pages: Optional[int] = Query(None, description="Limit the number of pages to scrape")
    proxy: Optional[str] = Query(None, description="Proxy string to use for scraping")

@app.post("/scrape")
async def scrape_catalogue(settings: ScrapeSettings):
    base_url = "https://dentalstall.com/shop/"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    proxy = {"http": settings.proxy, "https": settings.proxy} if settings.proxy else None

 # Clean the JSON file before running the script
    json_file_path = "scraped_data.json"
    if os.path.exists(json_file_path):
        with open(json_file_path, "w", encoding="utf-8") as file:
            json.dump([], file)

    scraped_data = []
    page = 1

    while True:
        if settings.limit_pages and page > settings.limit_pages:
            break

        url = f"{base_url}/page/{page}"
        response = requests.get(url, headers=headers, proxies=proxy)

        if response.status_code != 200:
            return {"error": f"Failed to fetch page {page}", "status_code": response.status_code}

        soup = BeautifulSoup(response.content, "html.parser")

        # Find all product elements
        products = soup.find_all("li", class_="product")
        if not products:
            break

        for product in products:
            name = product.find('h2', class_='woo-loop-product__title').get_text(strip=True) if product.find('h2', class_='woo-loop-product__title') else None
            price = product.find("span", class_="amount").get_text(strip=True) if product.find("span", class_="amount") else None
            image = product.find("img")["src"] if product.find("img") else None

            if name and price and image:
                scraped_data.append({
                    "product_title": name,
                    "product_price": float(price.replace('₹', '').strip()),
                    "path_to_image": image
                })

        page += 1

    # Save scraped data to a JSON file
    with open("scraped_data.json", "w", encoding="utf-8") as file:
        json.dump(scraped_data, file, indent=4)

    return {"message": "Scraping completed", "scraped_items": len(scraped_data)}
