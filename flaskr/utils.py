import pandas as pd
import datetime
import flaskr.tickers_dao as t_dao


def build_df(buffer):
    df = pd.DataFrame(data=buffer)
    df.index = df["fecha"]
    df.drop(['fecha'], axis=1, inplace=True)

    return df


def get_data_select_data_form(form_items):
    form_data = {}
    tickers_selected = []

    for k, v in form_items:
        if k == 'start':
            form_data['start_date'] = datetime.datetime.strptime(v, "%Y-%m-%d")
            continue

        if k == 'end':
            form_data['end_date'] = datetime.datetime.strptime(v, "%Y-%m-%d")
            continue

        if k == 'feature_select':
            form_data['feature'] = v
            continue

        if k == 'stock_select':
            form_data['stock_select'] = t_dao.get_ticker_byId(v)
            continue

        tickers_selected.append(t_dao.get_ticker_byId(k))

    form_data['tickers_selected'] = tickers_selected
    return form_data


# dict dfs
def reduce_data(data, feature):
    df_list = []

    for (stock, df) in data.items():
        to_drop = [col for col in df.columns if col != feature]

        df_list.append(
            df.drop(to_drop, axis=1).rename(columns={feature: stock})
        )

    if len(df_list) == 1:
        return df_list[0]

    return df_list[0].join(df_list[1:], how='outer')