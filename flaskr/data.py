import flaskr.market_data_dao as data_dao
import flaskr.api_controller as api_c
import time
from datetime import date


def process_tickers(tickers_selected, start_date, end_date):
    # dict dfs
    data = {}
    for ticker in tickers_selected:
        df_market = data_dao.get_data_byTickerCode(
            ticker.code,
            start_date=start_date,
            end_date=end_date
        )

        if df_market is not None:
            start_date_db = date.fromisoformat(
                df_market.index[0])

            end_date_db = date.fromisoformat(
                df_market.index[-1])

            if start_date_db <= date.fromisoformat(start_date)\
                    and end_date_db >= date.fromisoformat(end_date):
                print("No hace falta ir por datos")
                data[ticker.code] = df_market
                continue

        df_market = api_c.call_api(ticker.code, start_date, end_date)
        data_dao.save_data(df_market, ticker.code)
        data[ticker.code] = df_market
        time.sleep(15)

    return data
