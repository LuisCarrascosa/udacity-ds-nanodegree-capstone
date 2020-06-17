import pandas as pd


def build_df(buffer):
    df = pd.DataFrame(data=buffer)
    df.index = df["fecha"]
    df.drop(['fecha'], axis=1, inplace=True)

    return df


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
