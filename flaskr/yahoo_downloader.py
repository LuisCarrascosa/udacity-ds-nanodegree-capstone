import pandas as pd
import requests
import time
from io import StringIO
from datetime import datetime


def get_data(tickers):
    # fecha_fin = datetime(2020, 6, 15)
    fecha_fin = datetime.now().replace(hour=0, minute=0, second=0)
    period2 = int(fecha_fin.timestamp())

    url_1 = "https://query1.finance.yahoo.com/v7/finance/download"
    url_2 = "interval=1d&events=history"

    for ticker in tickers:
        fecha_ini = datetime.fromisoformat(ticker.last_date)
        print(f'{ticker.code}, {ticker.last_date}, {fecha_ini}')
        period1 = int(fecha_ini.timestamp())

        url = f"{url_1}/{ticker.code}?period1={period1}&period2={period2}&{url_2}"

        print(f'url: {url}')

        html = requests.get(url)
        bytes_data = html.content
        s = str(bytes_data, 'utf-8')
        buf = StringIO(s)

        ticker.df = pd.read_csv(buf)
        ticker.df.index = ticker.df["Date"]
        ticker.df.drop(['Date'], axis=1, inplace=True)

        with open(f'flaskr/raw_data/{ticker.code}.csv', 'w') as fo:
            print(buf.getvalue(), file=fo)

        time.sleep(1)

    return tickers
