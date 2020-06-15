from datetime import datetime
from flaskr.app_dto import MarketData


def alphavantage_daily_parser(ticker, json, limits=[]):
    output = []

    if len(limits) > 0 and len(limits) != 2:
        return None

    for date in list(json["Time Series (Daily)"]):
        fecha = datetime.strptime(date, '%Y-%m-%d')

        if fecha >= limits[0] and fecha <= limits[1]:
            output.insert(0, MarketData(
                {
                    'ticker_code': ticker,
                    'fecha': fecha,
                    'apertura':
                    float(json["Time Series (Daily)"][date]["1. open"]),
                    'maximo':
                    float(json["Time Series (Daily)"][date]["2. high"]),
                    'minimo':
                    float(json["Time Series (Daily)"][date]["3. low"]),
                    'cierre':
                    float(json["Time Series (Daily)"][date]["4. close"]),
                    'volumen':
                    float(json["Time Series (Daily)"][date]["5. volume"])
                }
            ))

    return output


def alphavantage_daily_variable_params(ticker):
    return {'symbol': ticker}


apis = {
    "alphavantage_daily": {
        "url": "https://www.alphavantage.co/query",
        "fixed_params": {
            "function": "TIME_SERIES_DAILY",
            "apikey": "FH7V7N94LF9QIZ61",
            "outputsize": "full"
        },
        "parser": alphavantage_daily_parser,
        "variable_params": alphavantage_daily_variable_params
    }
}


class Api:

    def __init__(self, name, url, fixed_params, parser, variable_params):
        self.name = name
        self.url = url
        self.fixed_params = fixed_params
        self.parser = parser
        self.variable_params = variable_params

    def get_url_params(self, ticker_name):
        return {**self.fixed_params, **self.variable_params(ticker_name)}


def get_api(api):
    return Api(
        api,
        apis[api]["url"],
        apis[api]["fixed_params"],
        apis[api]["parser"],
        apis[api]["variable_params"]
    )
