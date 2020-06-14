from flaskr.db import get_db
from flaskr.app_dto import Ticker


def selectAll():
    return get_db().execute(
        'SELECT id, code, ticker_name, currency, created FROM tickers'
    ).fetchall()


def get_ticker_byId(id):
    return Ticker(get_db().execute(
        'SELECT id, code, ticker_name, currency, api \
                FROM tickers WHERE id = ?', (id,)
    ).fetchone())


def get_ticker_byCode(code):
    print(code)
    return get_db().execute(
        'SELECT id, code, ticker_name, currency, api FROM tickers WHERE code = ?', (code,)
    ).fetchone()
