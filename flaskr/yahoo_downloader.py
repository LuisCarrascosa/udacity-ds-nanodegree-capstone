import pandas as pd
import requests
import time
from io import StringIO
from datetime import datetime


# 1594425600  1594598400
# 1594418400  1594591200
# https://query1.finance.yahoo.com/v7/finance/download/REP.MC?period1=1594425600&period2=1594598400&interval=1d&events=history
# REP.MC, fecha_ini: 2020-07-11 00:00:00, fecha_fin: 2020-07-13 00:00:00.559168
# REP.MC, period1: 1594418400, period2: 1594591200
def get_data(tickers):
    # fecha_fin = datetime(2020, 6, 15)
    fecha_fin = datetime.now().replace(hour=0, minute=0, second=0)
    period2 = int(fecha_fin.timestamp())

    url_1 = "https://query1.finance.yahoo.com/v7/finance/download"
    url_2 = "interval=1d&events=history"

    for ticker in tickers:
        fecha_ini = datetime.fromisoformat(ticker.last_date)
        period1 = int(fecha_ini.timestamp())
        print(f'{ticker.code}, fecha_ini: {fecha_ini}, fecha_fin: {fecha_fin}')
        print(f'{ticker.code}, period1: {period1}, period2: {period2}')

        url = f"{url_1}/{ticker.code}?period1={period1}&period2={period2}&{url_2}"

        print(f'url: {url}')

        html = requests.get(url)
        if html.status_code == 200:
            bytes_data = html.content
            s = str(bytes_data, 'utf-8')
            buf = StringIO(s)

            ticker.df = pd.read_csv(buf)
            ticker.df.index = ticker.df["Date"]
            ticker.df.drop(['Date'], axis=1, inplace=True)

            # with open(f'flaskr/raw_data/{ticker.code}.csv', 'w') as fo:
            #     print(buf.getvalue(), file=fo)

            time.sleep(1)
        else:
            print(f'{ticker.code} html.status_code: {html.status_code}')

    return tickers
