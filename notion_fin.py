import secrets
import yfinance as yf
import requests, json

DB_ID = secrets.DB_ID

query_headers = {
    "Authorization": secrets.KEY,
    "Notion-Version": "2021-05-13"
}
update_headers = {
    "Authorization": secrets.KEY,
    "Notion-Version": "2021-05-13",
    "Content-Type": "application/json"
}

query = {
    "filter": {
        "property": "Ticker"
    }
}

def get_tickers(database_id, query_headers, query):
    database_url = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = requests.request("POST", database_url, headers=query_headers, data=query)
    return response

def update_entry(page_id, headers, data):
    page_url = f"https://api.notion.com/v1/pages/{page_id}"
    response = requests.request("PATCH", page_url, headers=headers, data=data)
    return response

def update_notion_db(database_id, query_headers, update_headers, query):
    response = get_tickers(database_id, query_headers, query)
    for row in response.json()["results"]:
        stock = yf.Ticker(row["properties"]["Ticker"]["rich_text"][0]["plain_text"])
        price = stock.history(period='1m').Close[0]
        page_id = row["id"]
        
        data = {
            "properties": {
                "Price": {
                    "number": price
                }
            }
        }
        update_entry(page_id, update_headers, json.dumps(data))
        
update_notion_db(DB_ID, query_headers, update_headers, query)
