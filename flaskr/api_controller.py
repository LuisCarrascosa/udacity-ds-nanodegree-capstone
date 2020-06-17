import requests
import flaskr.api_factory as api_factory
import flaskr.tickers_dao as t_dao

from datetime import date


def call_api(ticker, start_date, end_date):
    ticker_dto = t_dao.get_ticker_byCode(ticker)
    api = api_factory.get_api(ticker_dto['api'])
    # api = api_factory.get_api('alphavantage_daily')
    json_data = requests.get(api.url, params=api.get_url_params(ticker)).json()

    return api.parser(ticker, json_data, limits=[
        date.fromisoformat(start_date),
        date.fromisoformat(end_date)])
