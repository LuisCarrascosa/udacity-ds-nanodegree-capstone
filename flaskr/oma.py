import pandas as pd
import numpy as np
import sqlite3
from tensorflow import keras


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


def getLastInput(data_set, stock, window_len):
    buffer = []
    cols = [col for col in list(data_set) if col != stock]

    temp_set = data_set[len(data_set) - window_len:][cols].copy()

    for col in list(temp_set):
        temp_set.loc[:, col] = temp_set[col]/temp_set[col].iloc[0] - 1

    buffer.append(np.array(temp_set))

    return np.array(buffer)


stock = "REP.MC"
window_len = 10
# pred_range = 5

db = create_connection("./instance/flaskr.sqlite")
df_0 = pd.read_sql('select * from luis', db)
db.close()

print(list(df_0["Fecha"])[-1].date().strftime("%Y-%m-%d"))
# print(df_0[len(df_0) - window_len:][stock])

# df_0.reset_index(inplace=True)
# df_0.drop(columns=['Fecha', 'index'], inplace=True)

# last_input = getLastInput(df_0, stock, window_len)
# model = keras.models.load_model('/home/luis/git/udacity-ds-nanodegree-capstone/models/1')
# print(model.summary())
# output_predicted = model.predict(last_input)
# r = df_0[len(df_0) - window_len:][stock].copy().iloc[0]
# print(r)
# output_predicted_unscaled = (output_predicted + 1) * r
# print(output_predicted_unscaled)

# 2702 2020-07-20   7.874
# 2703 2020-07-21   7.928
# 2704 2020-07-22   7.670

# 2695    7.624
# 2696    7.784
# 2697    7.986
# 2698    7.906
# 2699    8.014
# 2700    7.874
# 2701    7.874
# 2702    7.874
# 2703    7.928
# 2704    7.670

# Fecha	        Abrir	Máx.	Mín.	Cierre*	    Cierre ajus.**	Volumen
# 24 jul. 2020	7,50	7,54	7,39	7,39	    7,39	        7.528.641
# 23 jul. 2020	7,87	7,87	7,53	7,58	    7,58	        6.492.829

# 22 jul. 2020	7,85	7,92	7,64	7,67	    7,67	        7.345.795
