from flaskr.db import get_db
from flaskr.app_dto import Ticker


sql = 'SELECT id, code, ticker_name, currency, last_date \
                FROM tickers'


def selectAll():
    return [
        Ticker(row)
        for row in get_db().execute(sql).fetchall()
    ]


def get_outdated():
    return [
        Ticker(row)
        for row in get_db().execute(
            f"{sql} WHERE date(last_date) < date('now')"
            ).fetchall()
    ]


def get_ticker_byId(id):
    return Ticker(get_db().execute(
        f'{sql} WHERE id = ?', (id,)
    ).fetchone())


def get_ticker_byCode(code):
    return Ticker(get_db().execute(
        f'{sql} WHERE code = ?', (code,)
    ).fetchone())


def update_ticker(id):
    get_db().execute(
        "UPDATE tickers SET last_date = date('now') WHERE id = ?", (id,)
    )

    get_db().commit()
