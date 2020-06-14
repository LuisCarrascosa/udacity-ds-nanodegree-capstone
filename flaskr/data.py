import flaskr.market_data_dao as data_dao
import flaskr.api_controller as api_c
from datetime import datetime


def process_tickers(tickers_selected, start_date, end_date):
    # tickers --> (id, code, ticker_name, currency, created)[]
    data = {}
    for ticker in tickers_selected:
        market_data = data_dao.get_data_byTickerCode(
            ticker.code,
            start_date=start_date,
            end_date=end_date
        )

        if market_data is None or len(market_data) == 0:
            market_data = api_c.call_api(ticker, start_date, end_date)
            data_dao.save_data(ticker, market_data)
            continue
        elif market_data[0].fecha <= datetime.strptime(start_date, '%Y-%m-%d')\
                and market_data[-1].fecha > datetime.strptime(end_date, '%Y-%m-%d'):
            data[ticker] = market_data
            continue

        market_data = api_c.call_api(ticker, start_date, end_date)
        data_dao.save_data(ticker, market_data)


#     -- SELECT datetime(d1, "unixepoch")
#     FROM datetime_int
# CREATE TABLE market_data(
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     ticker_name TEXT NOT NULL,
#     fecha INTEGER NOT NULL,
#     apertura REAL NOT NULL,
#     maximo REAL NOT NULL,
#     minimo REAL NOT NULL,
#     cierre REAL NOT NULL,
#     volumen INTEGER,
#     created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY(ticker_name) REFERENCES tickers(ticker_name)
# )
