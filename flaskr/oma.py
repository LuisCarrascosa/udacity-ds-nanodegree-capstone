import pandas as pd
import numpy as np
import datetime
import sqlite3
from tensorflow import keras


def create_connection(db_file):
    db = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    return db


def getInputs(data_set, stock, window_len, pred_range):
    LSTM_training_inputs = []
    cols = [col for col in list(data_set) if col != stock]

    for i in range(1, len(data_set) - window_len - pred_range + 1):
        temp_set = data_set[i:(i+window_len)][cols].copy()

        for col in list(temp_set):
            temp_set.loc[:, col] = temp_set[col]/temp_set[col].iloc[0] - 1

        if temp_set.isnull().values.any():
            print('hay nans en el input')

        LSTM_training_inputs.append(temp_set)

    return LSTM_training_inputs


def getOutputs1(data_set, stock, window_len, pred_range):
    LSTM_training_outputs = []

    for i in range(window_len + 1, len(data_set[stock]) - pred_range + 1):
        temp_set = data_set[stock][i:i+pred_range].copy()

        LSTM_training_outputs.append(
            temp_set/data_set[stock].values[i-window_len] - 1
        )

    return LSTM_training_outputs


# model output is next 5 prices normalised to 10th previous closing price
def getOutputs(data_set, stock, window_len, pred_range):
    LSTM_training_outputs = []

    for i in range(window_len + 1, len(data_set[stock]) - pred_range + 1):
        LSTM_training_outputs.append(
            (
                data_set[stock][i:i+pred_range].values /
                data_set[stock].values[i-window_len]
            )-1
        )

    return np.array(LSTM_training_outputs)


def printDf(df):
    print(df.head(2))
    print(df.tail(2))


def getLastInput(data_set, stock, window_len):
    buffer = []
    cols = [col for col in list(data_set) if col != stock]

    temp_set = data_set[len(data_set) - window_len:][cols].copy()

    for col in list(temp_set):
        temp_set.loc[:, col] = temp_set[col]/temp_set[col].iloc[0] - 1

    buffer.append(np.array(temp_set))

    return np.array(buffer)


def getInput(df, stock, window_len, pred_range, fecha):
    LSTM_input = []

    last_i = df[df['Fecha'] == fecha].index[0]

    X_news = df[df['Fecha'] >= fecha]['Fecha']
    Y_news = df[df['Fecha'] >= fecha][stock]

    df.drop(['Fecha'], axis=1, inplace=True)
    x_set = df.iloc[last_i-window_len+1:last_i+1].copy()

    r_scale = dict()
    for col in list(x_set):
        r_scale[col] = x_set[col].iloc[0]
        x_set.loc[:, col] = x_set[col]/r_scale[col] - 1

    x_set.drop([stock], axis=1, inplace=True)
    LSTM_input.append(np.array(x_set))

    return last_i, r_scale, X_news, Y_news, np.array(LSTM_input)


# stock = "REP.MC"
# window_len = 40
# pred_range = 20
# feature = "cierre_ajustado"
# fecha = datetime.datetime(2020, 7, 22)

# db = create_connection("./instance/flaskr.sqlite")
# df_0 = pd.read_sql('select * from luis', db)
# db.close()

# last_i, r_scale, X_news, Y_news, LSTM_input = getInput(
#     df_0, stock, window_len, pred_range, fecha)

# model = keras.models.load_model(
#     '/home/luis/git/udacity-ds-nanodegree-capstone/models/1')

# prediction = (model.predict(LSTM_input) + 1) * r_scale[stock]

# print(X_news)
# print(Y_news)
# print(prediction[0])
# print(type(prediction[0]))

# (2089, 40, 14)
# (2089, 20)

# (2107, 40, 14)
# (2109,)

print([x for x in range(1,5)])