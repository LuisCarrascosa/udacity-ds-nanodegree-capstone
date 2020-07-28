from flask import (
    Blueprint, render_template, request, session, jsonify
)
from flaskr.auth import login_required
from keras.callbacks import LearningRateScheduler
import flaskr.market_data_dao as data_dao
# from datetime import date
import flaskr.learning_rate as learning_rate
import flaskr.painter as painter
import flaskr.users_dao as users_dao
import flaskr.model_data_dao as model_dao
import flaskr.utils as utils
import logging
import pickle
import numpy as np
import pandas as pd


bp = Blueprint('training', __name__, url_prefix='/training')
LOG = logging.getLogger(__name__)


# A training interface that accepts a data range
# (start_date, end_date) and a list of ticker symbols (e.g. GOOG, AAPL),
# and builds a model of stock behavior. Your code should read the
# desired historical prices from the data source of your choice.
@bp.route('/')
@login_required
def index():
    return render_template(
        'training/training.html',
        learning_rates=learning_rate.learning_rate_functions,
        learning_rate_selected='triangular',
        default_params=learning_rate.default_params
    )


@bp.route('/_learning_function', methods=['GET'])
@login_required
def _learning_function():
    learning_function = request.args.get(
        'learning_function_selected',
        'pepe',
        type=str
    )

    params = learning_rate.learning_rate_functions[learning_function]['params']
    return jsonify(params=params)


@bp.route('/_show_learning_function', methods=['POST'])
@login_required
def _show_learning_function():
    data_form = utils.get_training_form(request.get_json())

    if "inc_fraction" not in data_form:
        data_form["inc_fraction"] = 0

    schedule_function = utils.get_learning_function(data_form)

    schedule_name = learning_rate.learning_rate_functions[
        data_form["learning_rate_function"]
    ]["name"]

    graph_title = f"({schedule_name}) Learning rate for each epoch"

    base64_graph = painter.draw_learning_rate(
        schedule_function,
        graph_title, int(data_form["iterations"]))

    return jsonify(learning_graph=base64_graph)


@bp.route('/training', methods=['POST'])
@login_required
def training():
    form_stocks = pickle.loads(session['form_data'])
    stock = form_stocks['stock_select'].code
    window_len = int(request.form['window_len'])
    pred_range = int(request.form['pred_range'])

    df = data_dao.load_dataframe_table(
        users_dao.select_user_byId(
            session.get('user_id')
        )['username'])

    df.reset_index(inplace=True)

    resto = len(df) % (window_len + pred_range)
    df.drop([row for row in range(0, resto)], axis=0, inplace=True)

    df_rows = len(df)
    df.index = pd.RangeIndex(start=0, stop=df_rows, step=1)
    df_original = df.copy()

    df.drop(['Fecha'], axis=1, inplace=True)

    y_df = df[stock]
    x_df = df.drop([stock], axis=1, inplace=False)

    x_df_frames, y_df_frames = utils.get_frames(
        x_df, y_df, window_len, pred_range)

    rate = 0.8
    nrows_training = int(len(x_df_frames)*rate)
    df_x_training_frames = x_df_frames[0:nrows_training]
    df_x_test_frames = x_df_frames[nrows_training:]

    df_y_training_frames = y_df_frames[0:nrows_training]
    df_y_test_frames = y_df_frames[nrows_training:]

    LSTM_x_df_training_frames, LSTM_x_df_test_frames = utils.x_to_LSTM(
        df_x_training_frames, df_x_test_frames)

    LSTM_y_df_training_frames, LSTM_y_df_test_frames = utils.y_to_LSTM(
        df_y_training_frames, df_y_test_frames)

    # print(LSTM_x_df_training_frames[0].shape)
    # print(LSTM_y_df_training_frames.shape)

    training_form = utils.get_training_form(request.form)

    if "inc_fraction" not in training_form:
        training_form["inc_fraction"] = 0

    schedule_function = utils.get_learning_function(training_form)

    epochs = int(training_form['epochs'])
    neurons = int(training_form['number_neurons'])

    learningRateScheduler = LearningRateScheduler(schedule_function, verbose=0)

    # random seed for reproducibility
    np.random.seed(42)

    # initialise model architecture
    lstm_model = utils.build_model(
        LSTM_x_df_training_frames,
        output_size=pred_range,
        neurons=neurons,
        activ_func=training_form['activation_function'],
        dropout=training_form['dropout'],
        optimizer=training_form['optimizer_algorithm']
    )

    history = lstm_model.fit(
        LSTM_x_df_training_frames,
        LSTM_y_df_training_frames,
        epochs=epochs,
        batch_size=int(training_form['batch_size']),
        verbose=2,
        shuffle=True,
        validation_data=(LSTM_x_df_test_frames, LSTM_y_df_test_frames),
        use_multiprocessing=True,
        callbacks=[learningRateScheduler]
    )

    # df_original = data_dao.load_dataframe_table(
    #     users_dao.select_user_byId(
    #         session.get('user_id')
    #     )['username'])

    test_prediction = painter.draw_test_prediction(
        df_original,
        lstm_model,
        window_len,
        LSTM_x_df_test_frames,
        y_df,
        LSTM_y_df_test_frames,
        stock,
        pred_range,
        nrows_training
    )

    # test_prediction = painter.draw_single_timepoint_prediction(
    #     df_original,
    #     lstm_model,
    #     window_len,
    #     LSTM_test_inputs,
    #     test_set,
    #     stock
    # )

    lstm_model.save(f"models/{session.get('user_id')}")

    feature = form_stocks['feature']
    last_fecha = list(df_original["Fecha"])[-1].date().strftime("%Y-%m-%d")

    stock_select = form_stocks['stock_select']

    tickers_selected = [
        ticker for ticker in form_stocks['tickers_selected']
        if int(ticker.id) != int(stock_select.id)
        ]

    model_dao.save_model_data(
        tickers_selected,
        [int(stock_select.id)],
        window_len,
        pred_range,
        feature,
        last_fecha,
        int(session.get('user_id'))
    )

    return render_template(
        'training/training.html',
        learning_rates=learning_rate.learning_rate_functions,
        data_graph=painter.draw_losses(history),
        test_prediction=test_prediction,
        default_params=training_form
    )
