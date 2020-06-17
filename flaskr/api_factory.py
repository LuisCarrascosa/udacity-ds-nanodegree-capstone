from datetime import date
from flaskr.utils import build_df


def alphavantage_daily_parser(ticker, json, limits=[]):
    buffer = {
        'fecha': [],
        'apertura': [],
        'maximo': [],
        'minimo': [],
        'cierre': [],
        'volumen': []
    }

    if len(limits) > 0 and len(limits) != 2:
        return None

    for fecha_json in list(json["Time Series (Daily)"]):
        fecha = date.fromisoformat(fecha_json)

        if fecha >= limits[0] and fecha <= limits[1]:
            buffer['fecha'].insert(0, fecha)
            buffer['apertura'].insert(
                0, float(json["Time Series (Daily)"][fecha_json]["1. open"]))
            buffer['maximo'].insert(
                0, float(json["Time Series (Daily)"][fecha_json]["2. high"]))
            buffer['minimo'].insert(
                0, float(json["Time Series (Daily)"][fecha_json]["3. low"]))
            buffer['cierre'].insert(
                0, float(json["Time Series (Daily)"][fecha_json]["4. close"]))
            buffer['volumen'].insert(
                0, float(json["Time Series (Daily)"][fecha_json]["5. volume"]))

    return build_df(buffer)


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
