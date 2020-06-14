import sqlite3


storage = {}


def get_db():
    if 'db' not in storage:
        storage['db'] = sqlite3.connect(
            '/home/luis/git/udacity-ds-nanodegree-capstone/instance/flaskr.sqlite',
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # storage['db'].row_factory = sqlite3.Row

    return storage['db']


def close_db(e=None):
    db = storage.pop('db', None)

    if db is not None:
        db.close()


def get_data_byTickerCode(ticker, start_date=None, end_date=None):
    sql = 'SELECT id, ticker_code, fecha, apertura, maximo, minimo,\
                cierre, volumen, created,\
                MIN(fecha) as fecha_minimo, MAX(fecha) as fecha_maximo\
                FROM market_data WHERE ticker_code = ?'

    if start_date is None and end_date is None:
        return get_db().execute(sql, (ticker)).fetchall()

    if start_date is None:
        return get_db().execute(
            ' '.join([sql, 'AND fecha <= strftime("%s", ?)']),
            (ticker, end_date)
        ).fetchall()

    if end_date is None:
        return get_db().execute(
            ' '.join([sql, 'AND strftime("%s", ?) <= fecha']),
            (ticker, start_date)
        ).fetchall()

    query = ' '.join([sql,
                      'AND strftime("%s", ?) <= fecha',
                      'AND fecha <= strftime("%s", ?)'
                      ])

    return get_db().execute(
        query,
        (ticker, start_date, end_date)
    ).fetchone()


# 2020-06-08
# 2020-06-12
output = get_data_byTickerCode(
    'REP.MC', start_date='2020-06-08', end_date='2020-06-12')
print(output)

close_db()
