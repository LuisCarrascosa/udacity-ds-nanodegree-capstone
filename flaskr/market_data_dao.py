from flaskr.db import get_db
import flaskr.tickers_dao as tickers_dao
import datetime
import pandas as pd
import flaskr.utils as utils


def parse_df(sql_data_list):
    if sql_data_list is None or len(sql_data_list) == 0:
        return None

    buffer = {
        'fecha': [],
        'apertura': [],
        'maximo': [],
        'minimo': [],
        'cierre': [],
        'cierre_ajustado': [],
        'volumen': [],
        'id': []
    }

    for sql_data in sql_data_list:
        buffer['fecha'].append(sql_data['fecha'])
        buffer['apertura'].append(sql_data['apertura'])
        buffer['maximo'].append(sql_data['maximo'])
        buffer['minimo'].append(sql_data['minimo'])
        buffer['cierre'].append(sql_data['cierre'])
        buffer['cierre_ajustado'].append(sql_data['cierre_ajustado'])
        buffer['volumen'].append(sql_data['volumen'])
        buffer['id'].append(sql_data['id'])

    return utils.build_df(buffer)


# fecha, 'REP.MC', 'XOM'
# "2000-03-24"	"7.91791"	"21.087626"
# "2000-03-27"	"7.906283"	"20.887152"
def parse_df_feature(sql_data_list, tickers):
    if sql_data_list is None or len(sql_data_list) == 0:
        return None

    buffer = {'fecha': []}
    for ticker in tickers:
        buffer[ticker.code] = []

    for sql_data in sql_data_list:
        buffer['fecha'].append(
            datetime.datetime.strptime(sql_data['fecha'], "%Y-%m-%d")
        )

        for ticker in tickers:
            value = sql_data[ticker.code.replace('.', '_')]

            if value is None:
                buffer[ticker.code].append(None)
            else:
                buffer[ticker.code].append(float(value))

    return utils.build_df(buffer)


# dataframe: Date, Open, High, Low, Close, Adj Close, Volume
def save_data(tickers):
    for ticker in tickers:
        for ix in ticker.df.index:
            get_db().execute(
                "INSERT OR IGNORE INTO market_data \
                (ticker_id, fecha, apertura, maximo, minimo, cierre, \
                    cierre_ajustado, volumen) \
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    ticker.id,
                    ix,
                    ticker.df['Open'][ix],
                    ticker.df['High'][ix],
                    ticker.df['Low'][ix],
                    ticker.df['Close'][ix],
                    ticker.df['Adj Close'][ix],
                    ticker.df['Volume'][ix]
                )
            )

        tickers_dao.update_ticker(ticker.id)
        get_db().commit()


def get_data_on_feature(feature, tickers, start_date='2000-01-01',
                        end_date=None):
    grp_concat = [
        f"GROUP_CONCAT(case when md.ticker_id = {ticker.id} then md.{feature} else null end) as '{ticker.code.replace('.', '_')}'"
        for ticker in tickers]

    query = ''.join([
        'select date(md.fecha) as fecha, ',
        ', '.join(grp_concat),
        " from market_data md where md.ticker_id in (",
        ", ".join([str(ticker.id) for ticker in tickers]),
        ") AND date(md.fecha) >= date(?) AND date(md.fecha) <= date(?)",
        ' group by date(md.fecha)'
    ])

    print(f"Query: {query}")

    return parse_df_feature(
        get_db().execute(
            query, (start_date, end_date,)
            ).fetchall(), tickers
        )


def drop_dataframe_table(table_name):
    get_db().execute(f"DROP TABLE {table_name}")
    get_db().commit()


def save_dataframe_table(table_name, df):
    df.to_sql(
        table_name, get_db(), if_exists='replace',
        index=True, index_label='Fecha'
    )


def load_dataframe_table(table_name):
    return pd.read_sql(f'select * from {table_name}', get_db())
