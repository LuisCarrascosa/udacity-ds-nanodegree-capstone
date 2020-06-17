from flaskr.db import get_db
from flaskr.utils import build_df


def parse_df(sql_data_list):
    if sql_data_list is None or len(sql_data_list) == 0:
        return None

    buffer = {
        'fecha': [],
        'apertura': [],
        'maximo': [],
        'minimo': [],
        'cierre': [],
        'volumen': [],
        'id': []
    }

    for sql_data in sql_data_list:
        buffer['fecha'].append(sql_data['fecha'])
        buffer['apertura'].append(sql_data['apertura'])
        buffer['maximo'].append(sql_data['maximo'])
        buffer['minimo'].append(sql_data['minimo'])
        buffer['cierre'].append(sql_data['cierre'])
        buffer['volumen'].append(sql_data['volumen'])
        buffer['id'].append(sql_data['id'])

    return build_df(buffer)


def get_data_byTickerCode(ticker, start_date=None, end_date=None):
    sql = "SELECT id, ticker_code, date(fecha) as fecha,\
            apertura, maximo, minimo, cierre, volumen, created\
                FROM market_data WHERE ticker_code = ?"

    if start_date is None and end_date is None:
        query = ' '.join(sql, ['ORDER BY fecha ASC'])
        return parse_df(get_db().execute(query, (ticker,)).fetchall())

    if start_date is None:
        query = ' '.join([sql,
                          "AND fecha <= date(?)",
                          'ORDER BY fecha ASC'])

        return parse_df(get_db().execute(query, (ticker, end_date)).fetchall())

    if end_date is None:
        query = ' '.join([sql,
                          "AND date(?) <= fecha",
                          'ORDER BY fecha ASC'])

        return parse_df(get_db().execute(
            query, (ticker, start_date,)).fetchall()
        )

    query = ' '.join([sql,
                      "AND date(?) <= fecha",
                      "AND fecha <= date(?)",
                      'ORDER BY fecha ASC'
                      ])

    return parse_df(get_db().execute(
        query, (ticker, start_date, end_date)).fetchall()
    )


# dataframe
def save_data(df_market, ticker_code):
    for ix in df_market.index:
        get_db().execute(
            "INSERT OR IGNORE INTO market_data \
            (ticker_code, fecha, apertura, maximo, minimo, cierre, volumen) \
                VALUES (?, date(?), ?, ?, ?, ?, ?)",
            (
                ticker_code,
                ix,
                df_market['apertura'][ix],
                df_market['maximo'][ix],
                df_market['minimo'][ix],
                df_market['cierre'][ix],
                df_market['volumen'][ix])
        )

    get_db().commit()
