import pandas as pd
import numpy as np
import datetime
import sqlite3


def create_connection(db_file):
    db = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    return db


stock = "REP.MC"
window_len = 40
pred_range = 20
feature = "cierre_ajustado"
fecha = datetime.datetime(2020, 6, 25)

db = create_connection("./instance/flaskr.sqlite")
df_0 = pd.read_sql('select * from luis', db)
db.close()

print(df_0.shape)
print(df_0)
print("***********")

resto = len(df_0) % (window_len + pred_range)
rows_to_drop = [row for row in range(0, resto)]
df_0.drop(rows_to_drop, axis=0, inplace=True)
df_rows = len(df_0)

df_0.index = pd.RangeIndex(start=0, stop=df_rows, step=1)
df_orig = df_0.copy()
print("***********")
print(df_0)
df_0.drop(['Fecha'], axis=1, inplace=True)

y_df = df_0[stock]
x_df = df_0.drop([stock], axis=1, inplace=False)

x_df_frames = []
y_df_frames = []
for i in range(0, df_rows - window_len - pred_range + 1):
    x_temp_set = x_df[i:(i+window_len)].copy()

    for col in list(x_temp_set):
        x_temp_set.loc[:, col] = x_temp_set[col]/x_temp_set[col].iloc[0] - 1

    x_df_frames.append(x_temp_set)

    y_df_frames.append(
        (
            y_df[i+window_len:i+window_len+pred_range].to_numpy() /
            y_df.to_numpy()[i]
        )-1
    )

# print(y_df[41:45])
# print("******************")
# print(y_df[1:2])
# print("******************")
# print(y_df_frames[1])
# print("******************")

n_frames = len(x_df_frames)
# print(n_frames)

nrows_training = int(n_frames*0.8)
# print(nrows_training)

x_df_training_frames = x_df_frames[0:nrows_training]
x_df_test_frames = x_df_frames[nrows_training:]

y_df_training_frames = y_df_frames[0:nrows_training]
y_df_test_frames = y_df_frames[nrows_training:]

LSTM_x_df_training_frames = [
    np.array(x_df_training_frame)
    for x_df_training_frame in x_df_training_frames
]

LSTM_x_df_test_frames = [
    np.array(x_df_test_frame)
    for x_df_test_frame in x_df_test_frames
]

LSTM_y_df_training_frames = np.array(y_df_training_frames)
LSTM_y_df_test_frames = np.array(y_df_test_frames)

# (
#     y_df[i+window_len:i+window_len+pred_range].to_numpy() /
#     y_df.to_numpy()[i]
# )-1
# y_df_test_frames = y_df_frames[nrows_training:]
# print(LSTM_y_df_test_frames[0])
# print("******************")
# print(y_df_test_frames[0])
# print("******************")
# print(y_df_frames[nrows_training])
# print("******************")
# print(y_df[nrows_training+window_len:nrows_training+window_len+pred_range].to_numpy())
# print("******************")
# print(y_df.to_numpy()[nrows_training])
print(df_orig.iloc[y_df[nrows_training:].index])
print(y_df.tail())
print(df_orig.tail())
