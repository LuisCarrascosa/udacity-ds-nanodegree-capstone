from flask import (
    Blueprint, render_template, request, session, jsonify
)
from flaskr.auth import login_required
# from datetime import date
import flaskr.learning_rate as learning_rate
import flaskr.painter as painter
import logging
import pickle


bp = Blueprint('training', __name__, url_prefix='/training')
LOG = logging.getLogger(__name__)


# A training interface that accepts a data range
# (start_date, end_date) and a list of ticker symbols (e.g. GOOG, AAPL),
# and builds a model of stock behavior. Your code should read the
# desired historical prices from the data source of your choice.
@bp.route('/')
@login_required
def index():
    # form_data = pickle.loads(session['form_data'])

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
    data = request.get_json()

    parsed_data = {
        k: float(v)
        for (k, v) in data.items()
        if k != 'learning_rate_function'
    }

    schedule_function = learning_rate.learning_rate_functions[
        data["learning_rate_function"]
        ]["function"]

    schedule_name = learning_rate.learning_rate_functions[
        data["learning_rate_function"]
        ]["name"]

    schedule_function = learning_rate.CyclicalSchedule(
        schedule_function,
        min_lr=parsed_data["min_lr"],
        max_lr=parsed_data["max_lr"],
        cycle_length=int(parsed_data["iterations"]/parsed_data["num_cycles"]),
        cycle_length_decay=parsed_data["cycle_length_decay"],
        cycle_magnitude_decay=parsed_data["cycle_magnitude_decay"],
        inc_fraction=parsed_data["inc_fraction"]
    )

    graph_title = f"({schedule_name}) Learning rate for each epoch"

    base64_graph = painter.draw_learning_rate(
        schedule_function,
        graph_title, int(parsed_data["iterations"]))

    # print(f"base64_graph: {base64_graph}")

    return jsonify(learning_graph=base64_graph)


# Hyperparameters related to neural network structure
# 1. Number of hidden layers – adding more hidden layers of neurons
# generally improves accuracy, to a certain limit which can differ depending
# on the problem.

# 2. Dropout – what percentage of neurons should be randomly “killed” during
# each epoch to prevent overfitting.

# 3. Neural network activation function – which function should be used to
# process the inputs flowing into each neuron. The activation function can
# impact the network’s ability to converge and learn for different ranges of
# input values, and also its training speed.

# 4. Weights initialization – it is necessary to set initial weights for the
# first forward pass. Two basic options are to set weights to zero or to
# randomize them. However, this can result in a vanishing or exploding
# gradient, which will make it difficult to train the model. To mitigate this
# problem, you can use a heuristic (a formula tied to the number of neuron
# layers) to determine the weights. A common heuristic used for the Tanh
# activation is called Xavier initialization.

# Hyperparameters related to training algorithm
# 5. Neural network learning rate – how fast the backpropagation algorithm
# performs gradient descent. A lower learning rate makes the network train
# faster but might result in missing the minimum of the loss function.


# 6. Deep learning epoch, iterations and batch size – these parameters
# determine the rate at which samples are fed to the model for training. An
# epoch is a group of samples which are passed through the model together
# (forward pass) and then run through backpropagation (backward pass) to
# determine their optimal weights. If the epoch cannot be run all together
# due the size of the sample or complexity of the network, it is split into
# batches, and the epoch is run in two or more iterations. The number of
# epochs and batches per epoch can significantly affect model fit, as shown
# below.

# 7. Optimizer algorithm and neural network momentum – when a neural network
# trains, it uses an algorithm to determine the optimal weights for the model,
# called an optimizer. The basic option is Stochastic Gradient Descent, but
# there are other options. Another common algorithm is Momentum, which works
# by waiting after a weight is updated, and updating it a second time using a
# delta amount. This speeds up training gradually, with a reduced risk of
# oscillation. Other algorithms are Nesterov Accelerated Gradient,
# AdaDelta and Adam.

# activation ReLU, Leaky ReLU, Swish
# window_len, 80%, output_size, neurons
# dropout =0.25, loss="mae", optimizer="adam", batch_size=1
@bp.route('/training', methods=['POST'])
@login_required
def training():
    form_data = pickle.loads(session['form_data'])

    return render_template(
        'training/training.html',
        start_date=form_data['end_date']
    )


@bp.route('/save', methods=['POST'])
@login_required
def save():
    form_data = pickle.loads(session['form_data'])

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
