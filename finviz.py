import json
import requests
import pandas as pd
import numpy as np
import itertools
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


AUTH_HEADER = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
  "X-Requested-With": "XMLHttpRequest"
}

def read_stock_info(ticker) -> dict:
    r = requests.get(f"https://finviz.com/quote.ashx?t={ticker}", headers=AUTH_HEADER)
    
    if r.status_code != 404:
        soup = BeautifulSoup(r.text, 'lxml')
        financial_info = str(soup.find("table",{"class":"snapshot-table2"}))
        finance_df = pd.read_html(str(financial_info), )[0]

        finance_json = json.loads(finance_df.to_json(orient="values"))
        flat_list = list(itertools.chain(*finance_json))
        it = iter(flat_list)
        data_map = dict(zip(it, it))
        data_map["STOCK_TICKER"] = ticker
        return data_map

    return None

def read_tickers_parallel(tickers):
    pool = ThreadPoolExecutor(max_workers=2)
    result = []
    for ticker_data in pool.map(read_stock_info, tickers):
       if(ticker_data is not None):
        print(ticker_data["STOCK_TICKER"])
        result.append(ticker_data)

    return result

def save_data_to_file(name, data):
    with open(f'./data/{name}.json', 'w+', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data_from_file(name):
    with open(f'./data/{name}.json', 'r', encoding='utf-8') as f:
        return json.load(f)