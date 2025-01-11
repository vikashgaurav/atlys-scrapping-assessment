# Atlys Scrapping Assessment

This project uses the Python FastAPI framework to automate the process of scraping product information from a website. It exposes an API endpoint to trigger the scraping operation and retrieve the collected data in a structured format.

## Features

- Automatically scrape product details such as name and price from multiple pages.
- Configurable to limit the number of pages scraped.
- Option to use a proxy for scraping requests.

## Steps to Run

Follow these instructions to set up and run the project:

### 1. Install Dependencies

First, install the required dependencies listed in the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 2. Run the FastAPI Server
```
uvicorn scraper:app --reload
```

This will run the FastAPI app locally at http://127.0.0.1:8000.

### 3. Test the POST API

#### URL: http://127.0.0.1:8000/scrape

#### HTTP Method:POST

#### Request Body (JSON):

```json
    {
        "limit_pages": 5,
        "proxy": null
    }
```

#### Response
```json
    {
        "message": "Scraping completed",
        "scraped_items": 120
    }
```
