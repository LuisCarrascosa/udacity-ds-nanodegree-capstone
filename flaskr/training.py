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
import flaskr.utils as utils
import logging
import pickle
import numpy as np
import tensorflow as tf
from tensorflow import keras


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

    df = data_dao.load_dataframe_table(
        users_dao.select_user_byId(
            session.get('user_id')
        )['username'])

    df.reset_index(inplace=True)
    df.drop(columns=['Fecha', 'index'], inplace=True)

    print(f'df.isna().sum(): {df.isna().sum()}')

    nrows_training = int(df.shape[0]*0.8)

    training_set = df[df.index < nrows_training]
    test_set = df[df.index >= nrows_training]

    window_len = int(request.form['window_len'])
    pred_range = int(request.form['pred_range'])

    LSTM_training_inputs = utils.getInputs(
        training_set, stock, window_len, pred_range)

    LSTM_training_outputs = utils.getOutputs(
        training_set, stock, window_len, pred_range)

    LSTM_test_inputs = utils.getInputs(test_set, stock, window_len, pred_range)

    LSTM_test_outputs = utils.getOutputs(
        test_set, stock, window_len, pred_range)

    LSTM_training_inputs = [
        np.array(LSTM_training_input)
        for LSTM_training_input in LSTM_training_inputs
    ]

    LSTM_training_inputs = np.array(LSTM_training_inputs)

    LSTM_test_inputs = [
        np.array(LSTM_test_inputs)
        for LSTM_test_inputs in LSTM_test_inputs
    ]

    LSTM_test_inputs = np.array(LSTM_test_inputs)

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
        LSTM_training_inputs,
        output_size=pred_range,
        neurons=neurons,
        activ_func=training_form['activation_function'],
        dropout=training_form['dropout'],
        optimizer=training_form['optimizer_algorithm']
    )

    history = lstm_model.fit(
        LSTM_training_inputs,
        LSTM_training_outputs,
        epochs=epochs,
        batch_size=int(training_form['batch_size']),
        verbose=2,
        shuffle=True,
        validation_data=(LSTM_test_inputs, LSTM_test_outputs),
        use_multiprocessing=True,
        callbacks=[learningRateScheduler]
    )

    df_original = data_dao.load_dataframe_table(
        users_dao.select_user_byId(
            session.get('user_id')
        )['username'])

    test_prediction = painter.draw_test_prediction(
        df_original,
        lstm_model,
        window_len,
        LSTM_test_inputs,
        test_set,
        stock,
        pred_range
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

    return render_template(
        'training/training.html',
        learning_rates=learning_rate.learning_rate_functions,
        data_graph=painter.draw_losses(history),
        test_prediction=test_prediction,
        default_params=training_form
    )


@bp.route('/save', methods=['POST'])
@login_required
def save():
    # Volver al inicio
    return render_template(
        'training/training.html',
        start_date=form_data['end_date']
    )

# from tensorflow.keras import layers
# from tensorflow.keras import activations
# import tensorflow as tf

# model.add(layers.Dense(64))
# model.add(layers.Activation(tf.keras.activations.swish))
# model.add(layers.Activation(tf.nn.))

# def create_model():
#     lstm_model = Sequential()
#     # (batch_size, timesteps, data_dim)
#     lstm_model.add(LSTM(100, batch_input_shape=(BATCH_SIZE, TIME_STEPS, x_t.shape[2]),
#                         dropout=0.0, recurrent_dropout=0.0, stateful=True, return_sequences=True,
#                         kernel_initializer='random_uniform'))
#     lstm_model.add(Dropout(0.4))
#     lstm_model.add(LSTM(60, dropout=0.0))
#     lstm_model.add(Dropout(0.4))
#     lstm_model.add(Dense(20,activation='relu'))
#     lstm_model.add(Dense(1,activation='sigmoid'))
#     optimizer = optimizers.RMSprop(lr=params["lr"])
#     # optimizer = optimizers.SGD(lr=0.000001, decay=1e-6, momentum=0.9, nesterov=True)
#     lstm_model.compile(loss='mean_squared_error', optimizer=optimizer)
#     return lstm_model
