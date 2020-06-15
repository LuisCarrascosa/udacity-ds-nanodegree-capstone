from flaskr.db import get_db


def get_data_byTickerCode(ticker, start_date=None, end_date=None):
    sql = "SELECT id, ticker_code, date(fecha) as fecha,\
            apertura, maximo, minimo, cierre, volumen, created\
                FROM market_data WHERE ticker_code = ?"

    if start_date is None and end_date is None:
        query = ' '.join(sql, ['ORDER BY fecha ASC'])
        return get_db().execute(query, (ticker,)).fetchall()

    if start_date is None:
        query = ' '.join([sql,
                          "AND fecha <= date(?)",
                          'ORDER BY fecha ASC'])

        return get_db().execute(query, (ticker, end_date)).fetchall()

    if end_date is None:
        query = ' '.join([sql,
                          "AND date(?) <= fecha",
                          'ORDER BY fecha ASC'])

        return get_db().execute(query, (ticker, start_date,)).fetchall()

    query = ' '.join([sql,
                      "AND date(?) <= fecha",
                      "AND fecha <= date(?)",
                      'ORDER BY fecha ASC'
                      ])

    return get_db().execute(query, (ticker, start_date, end_date)).fetchall()


def save_data(market_data):
    for data in market_data:
        get_db().execute(
            "INSERT OR IGNORE INTO market_data \
            (ticker_code, fecha, apertura, maximo, minimo, cierre, volumen) \
                VALUES (?, date(?), ?, ?, ?, ?, ?)",
            (
                data.ticker_code,
                data.fecha,
                data.apertura,
                data.maximo,
                data.minimo,
                data.cierre,
                data.volumen)
        )

    get_db().commit()
