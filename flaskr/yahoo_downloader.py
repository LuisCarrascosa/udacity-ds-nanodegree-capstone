import pandas as pd
import requests
from io import StringIO
from datetime import datetime, time


def get_data(tickers, start_date='2000-01-01', end_date=None):
    data = []

    fecha_ini = datetime.fromisoformat(start_date)
    fecha_fin = datetime.datetime.now().replace(hour=0, minute=0, second=0)

    period1 = int(fecha_ini.timestamp())
    period2 = int(fecha_fin.timestamp())

    url_1 = "https://query1.finance.yahoo.com/v7/finance/download"
    url_2 = "interval=1d&events=history"

    for ticker in tickers:
        url = f"{url_1}/{ticker}?period1={period1}&period2={period2}&{url_2}"
        # print(url)

        html = requests.get(url)
        bytes_data = html.content
        s = str(bytes_data, 'utf-8')

        data[ticker] = pd.read_csv(StringIO(s))
        time.sleep(2)

    return data
