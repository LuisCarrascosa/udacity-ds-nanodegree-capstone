from flaskr.db import get_db


def get_data_byTickerCode(ticker, start_date=None, end_date=None):
    sql = "SELECT id, ticker_code, datetime(fecha,'localtime') as fecha,\
            apertura, maximo, minimo, cierre, volumen, created\
                FROM market_data WHERE ticker_code = ?"

    print(start_date)
    print(end_date)
    print(ticker)

    if start_date is None and end_date is None:
        query = ' '.join(sql, ['ORDER BY fecha ASC'])
        return get_db().execute(query, (ticker,)).fetchall()

    if start_date is None:
        query = ' '.join([sql,
                          "AND fecha <= datetime(?,'localtime')",
                          'ORDER BY fecha ASC'])

        return get_db().execute(query, (ticker, end_date)).fetchall()

    if end_date is None:
        query = ' '.join([sql,
                          "AND datetime(?,'localtime') <= fecha",
                          'ORDER BY fecha ASC'])

        return get_db().execute(query, (ticker, start_date,)).fetchall()

    query = ' '.join([sql,
                      "AND datetime(?,'localtime') <= fecha",
                      "AND fecha <= datetime(?,'localtime')",
                      'ORDER BY fecha ASC'
                      ])

    return get_db().execute(query, (ticker, start_date, end_date)).fetchall()


def save_data(ticker, market_data):
    for data in market_data:
        get_db().execute(
            "INSERT INTO market_data \
            (ticker_code, fecha, apertura, maximo, minimo, cierre, volumen) \
                VALUES (?, datetime(?,'localtime'), ?, ?, ?, ?, ?)",
            (
                data.ticker_name,
                data.fecha,
                data.apertura,
                data.maximo,
                data.minimo,
                data.cierre,
                data.volumen)
        )

    get_db().commit()
