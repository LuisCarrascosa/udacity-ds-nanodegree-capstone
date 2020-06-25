import flaskr.market_data_dao as data_dao
import flaskr.api_controller as api_c
import time
from datetime import date


def process_tickers(tickers_selected, start_date, end_date):
    # dict dfs
    data = {}
    for ticker in tickers_selected:
        df_market = data_dao.get_data_byTickerCode(
            ticker.code, end_date=end_date
        )

        if df_market is None:
            df_market = api_c.call_api(ticker.code, '2000-01-01', end_date)
            time.sleep(2)
        else:
            end_date_db = date.fromisoformat(df_market.index[-1])

            if end_date_db >= date.fromisoformat(end_date):
                print("No hace falta ir por datos")
            else:
                df_market = api_c.call_api(ticker.code, start_date, end_date)
        
        data_dao.save_data(df_market, ticker.code)
        data[ticker.code] = df_market
        time.sleep(2)

    return data
