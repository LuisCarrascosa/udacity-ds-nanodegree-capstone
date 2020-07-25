from keras.models import Sequential
from keras.layers import Activation, Dense, LSTM, Dropout, LeakyReLU
import pandas as pd
import datetime
import pickle
import numpy as np
import flaskr.learning_rate as learning_rate
import flaskr.tickers_dao as t_dao
import flaskr.market_data_dao as data_dao
import flaskr.users_dao as users_dao


# https://machinelearningmastery.com/convert-time-series-supervised-learning-problem-python/
# https://machinelearningmastery.com/multivariate-time-series-forecasting-lstms-keras/
# https://machinelearningmastery.com/tune-lstm-hyperparameters-keras-time-series-forecasting/
# https://machinelearningmastery.com/difference-between-a-batch-and-an-epoch/
def build_model(inputs, output_size, neurons, activ_func, dropout,
                optimizer, loss="mae"):
    model = Sequential()

    model.add(LSTM(neurons, input_shape=(inputs.shape[1], inputs.shape[2])))
    model.add(Dropout(dropout))
    model.add(Dense(units=output_size))

    if activ_func == 'leaky_relu':
        model.add(LeakyReLU(alpha=0.1))
    else:
        model.add(Activation(activ_func))  # linear, softmax, tanh

    model.compile(loss=loss, optimizer=optimizer)
    return model


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


def save_session(session, form_data, df):
    if 'form_data' in session:
        session.pop('form_data', None)

    print(f"USUARIO: {session.get('user_id')}")
    data_dao.save_dataframe_table(
        users_dao.select_user_byId(session.get('user_id'))['username'],
        df
    )

    form_data_serialized = pickle.dumps(form_data)
    session['form_data'] = form_data_serialized


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


def get_training_form(data_dict):
    return {
        k: (
            float(v) if k not in (
                'learning_rate_function',
                'activation_function',
                'initial_weights',
                'optimizer_algorithm'
            )
            else v
        )
        for k, v in data_dict.items()
    }


def get_learning_function(data_dict):
    schedule_function = learning_rate.learning_rate_functions[
        data_dict["learning_rate_function"]
    ]["function"]

    return learning_rate.CyclicalSchedule(
        schedule_function,
        min_lr=data_dict["min_lr"],
        max_lr=data_dict["max_lr"],
        cycle_length=int(data_dict["iterations"]/data_dict["num_cycles"]),
        cycle_length_decay=data_dict["cycle_length_decay"],
        cycle_magnitude_decay=data_dict["cycle_magnitude_decay"],
        inc_fraction=data_dict["inc_fraction"]
    )
