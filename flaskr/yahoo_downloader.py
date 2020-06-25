import pandas as pd
import datetime
import pytz
import requests
from io import StringIO


ticker = 'ELE.MC'
# https://query1.finance.yahoo.com/v7/finance/download/ELE.MC?period1=1104537600&period2=1593043200&interval=1d&events=history
fecha_ini = datetime.datetime(2005, 1, 1)
fecha_fin = datetime.datetime(2020, 6, 26)

period1 = int(pytz.utc.localize(fecha_ini).timestamp())
period2 = int(pytz.utc.localize(fecha_fin).timestamp())

url = f"https://query1.finance.yahoo.com/v7/finance/download/{ticker}?period1={period1}&period2={period2}&interval=1d&events=history"
print(url)

html = requests.get(url)
bytes_data = html.content
s = str(bytes_data, 'utf-8')

df = pd.read_csv(StringIO(s))
print(df)
