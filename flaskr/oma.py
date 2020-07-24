import pandas as pd
import numpy as np
import sqlite3


def create_connection(db_file):
    db = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES)
    db.row_factory = sqlite3.Row
    return db


def series_to_supervised(data, n_in=1, n_out=1, dropnan=True):
    n_vars = 1 if type(data) is list else data.shape[1]
    df = pd.DataFrame(data)
    cols, names = list(), list()
    # input sequence (t-n, ... t-1)
    for i in range(n_in, 0, -1):
        cols.append(df.shift(i))
        names += [('var%d(t-%d)' % (j+1, i)) for j in range(n_vars)]
    # forecast sequence (t, t+1, ... t+n)
    for i in range(0, n_out):
        cols.append(df.shift(-i))
        if i == 0:
            names += [('var%d(t)' % (j+1)) for j in range(n_vars)]
        else:
            names += [('var%d(t+%d)' % (j+1, i)) for j in range(n_vars)]
    # put it all together
    agg = pd.concat(cols, axis=1)
    agg.columns = names
    # drop rows with NaN values
    if dropnan:
        agg.dropna(inplace=True)
    return agg


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
                data_set[stock][i:i+pred_range].values/data_set[stock].values[i-window_len]
            )-1
        )

    return np.array(LSTM_training_outputs)


def printDf(df):
    print(df.head(2))
    print(df.tail(2))


db = create_connection("./instance/flaskr.sqlite")
df_0 = pd.read_sql('select * from luis', db)
db.close()

# df_0.index = df_0["Fecha"]
df_0.drop(['Fecha'], axis=1, inplace=True)
# values = df_0.values

stock = "REP.MC"
window_len = 10
pred_range = 5

# print(df_0.tail(20))
print(df_0[stock][0])

print(df_0.shape)
inputs = getInputs(df_0, stock, window_len, pred_range)

print(inputs[:-pred_range])

# print(f"0 input: {inputs[0]}")
# print(f"1 input: {inputs[1]}")
# print(f"-5 input: {inputs[-5]}")
# print(f"-2 input: {inputs[-2]}")
# print(f"-1 input: {inputs[-1]}")

# print(f"len inputs: {len(inputs)}")
# print(f"shape inputs: {inputs[0].shape}")

# outputs = getOutputs(df_0, stock, window_len, pred_range)
# # outputs = getOutputs1(df_0, stock, window_len, pred_range)
# # print(f"shape outputs: {outputs.shape}")
# print(f"0 output: {outputs[0]}")
# print(f"1 output: {outputs[1]}")
# print(f"-2 output: {outputs[-2]}")
# print(f"-1 output: {outputs[-1]}")
