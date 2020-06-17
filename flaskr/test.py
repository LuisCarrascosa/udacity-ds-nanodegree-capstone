import itertools
import pandas as pd


def build_df(buffer):
    df = pd.DataFrame(data=buffer)
    df.index = df["fecha"]
    df.drop(['fecha'], axis=1, inplace=True)

    return df


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


buffer1 = {
    'fecha': ['2020-06-01', '2020-06-02', '2020-06-03'],
    'apertura': ['ap11_b1', 'ap12_b1', 'ap13_b1'],
    'cierre': ['ci21_b1', 'ci22_b1', 'ci23_b1']
}

# buffer2 = {
#     'fecha': ['2020-06-01', '2020-06-02', '2020-06-03'],
#     'apertura': ['ap11_b2', 'ap12_b2', 'ap13_b2'],
#     'cierre': ['ci21_b2', 'ci22_b2', 'ci23_b2']
# }

buffer2 = {
    'fecha': ['2020-06-01', '2020-06-03'],
    'apertura': ['ap11_b2', 'ap13_b2'],
    'cierre': ['ci21_b2', 'ci23_b2']
}

buffer3 = {
    'fecha': ['2020-06-01', '2020-06-02', '2020-06-03'],
    'apertura': ['ap11_b3', 'ap12_b3', 'ap13_b3'],
    'cierre': ['ci21_b3', 'ci22_b3', 'ci23_b3']
}

df1 = build_df(buffer1)
df2 = build_df(buffer2)
df3 = build_df(buffer3)

data = {'STOCK1': df1, 'STOCK2': df2, 'STOCK3': df3}
# print(data)

df_result = reduce_data(data, 'cierre')
print(df_result)

# for (k, v) in buffer3.items():
#     print(f'{k}, {v}')
