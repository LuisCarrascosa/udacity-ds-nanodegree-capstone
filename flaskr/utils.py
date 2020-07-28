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


def get_frames(x_df, y_df, window_len, pred_range):
    x_df_frames = []
    y_df_frames = []

    for i in range(0, len(x_df) - window_len - pred_range + 1):
        x_temp_set = x_df[i:(i+window_len)].copy()

        for col in list(x_temp_set):
            x_temp_set.loc[:, col] = x_temp_set[col] / \
                x_temp_set[col].iloc[0] - 1

        x_df_frames.append(x_temp_set)

        y_df_frames.append(
            (
                y_df[i+window_len:i+window_len+pred_range].to_numpy() /
                y_df.to_numpy()[i]
            )-1
        )

    return x_df_frames, y_df_frames


# LSTM_training_inputs = [np.array(LSTM_training_input) for LSTM_training_input in LSTM_training_inputs]
# LSTM_training_inputs = np.array(LSTM_training_inputs)
def x_to_LSTM(df_x_training_frames, df_x_test_frames):
    LSTM_x_df_training_frames = [
        np.array(x_df_training_frame)
        for x_df_training_frame in df_x_training_frames
    ]

    LSTM_x_df_test_frames = [
        np.array(x_df_test_frame)
        for x_df_test_frame in df_x_test_frames
    ]

    return np.array(LSTM_x_df_training_frames), np.array(LSTM_x_df_test_frames)


def y_to_LSTM(df_y_training_frames, df_y_test_frames):
    return np.array(df_y_training_frames), np.array(df_y_test_frames)


def getInputs(data_set, stock, window_len, pred_range):
    LSTM_training_inputs = []
    cols = [col for col in list(data_set) if col != stock]

    for i in range(0, len(data_set) - window_len):
        temp_set = data_set[i:(i+window_len)][cols].copy()

        for col in list(temp_set):
            temp_set.loc[:, col] = temp_set[col]/temp_set[col].iloc[0] - 1

        if temp_set.isnull().values.any():
            print('hay nans en el input')

        LSTM_training_inputs.append(temp_set)

    return LSTM_training_inputs


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


# model output is next 5 prices normalised to 10th previous closing price
def getOutputs(data_set, stock, window_len, pred_range):
    LSTM_training_outputs = []

    for i in range(window_len, len(data_set[stock])):
        LSTM_training_outputs.append(
            (
                data_set[stock][i:i+pred_range].to_numpy() /
                data_set[stock].values[i-window_len]
            )-1
        )

    return LSTM_training_outputs


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


features = {
    "apertura": "Open",
    "maximo": "High",
    "minimo": "Low",
    "cierre": "Close",
    "cierre_ajustado": "Adj Close"
}


def get_feature_description(feature):
    return features[feature]
