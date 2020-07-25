from flaskr.db import get_db


def save_model_data(
    x_tickers, y_tickers, window_len, pred_range, feature, last_fecha, id_user
):
    get_db().execute("DELETE FROM models_data WHERE id = ?", (id_user,))

    get_db().execute(
        "DELETE FROM models_x_tickers WHERE models_id = ?", (id_user,))

    get_db().execute("INSERT INTO models_data (id, pred_range, window_len, feature, fecha)\
        VALUES (?, ?, ?, ?, ?)",
                     (id_user, pred_range, window_len, feature, last_fecha)
                     )

    for x_ticker in x_tickers:
        get_db().execute("INSERT INTO models_x_tickers (models_id, ticker_id, ticker_type)\
            VALUES (?, ?, ?)", (id_user, x_ticker, "X"))

    for y_ticker in y_tickers:
        get_db().execute("INSERT INTO models_x_tickers (models_id, ticker_id, ticker_type)\
            VALUES (?, ?, ?)", (id_user, y_ticker, "Y"))

    get_db().commit()


def load_model_data(id_user):
    user_model_data = get_db().execute(
        'SELECT pred_range, window_len, feature, fecha\
            FROM models_data WHERE id = ?', (id_user,)
    ).fetchone()

    models_x_tickers = get_db().execute(
        "select mxt.ticker_type as ticker_type, tck.code as code\
        from models_x_tickers mxt inner join tickers tck\
        on tck.id = mxt.ticker_id and mxt.models_id = ?",
        (id_user,)
    ).fetchall()

    x_stocks = []
    y_stocks = []
    for ticker in models_x_tickers:
        if ticker['ticker_type'] == 'X':
            x_stocks.append(ticker['code'])

        if ticker['ticker_type'] == 'Y':
            y_stocks.append(ticker['code'])

    return user_model_data, x_stocks, y_stocks
