import base64
# import datetime
import numpy as np
from io import BytesIO
from matplotlib.figure import Figure


# title(dataset.columns[group], y=0.5, loc='right')
def drawFeatures_byDict(df, nrows, ncols, tickers, f_ini=None, f_fin=None):
    fig = Figure(figsize=(6, 2.45*nrows), dpi=200)

    i = 1
    for ticker in tickers:
        axis = fig.add_subplot(nrows, ncols, i, label=ticker.ticker_name)

        if f_ini is None or f_fin is None:
            axis.plot(df[ticker.code])
        else:
            axis.plot(df[ticker.code].loc[f_ini:f_fin])

        axis.grid(True)
        axis.autoscale_view()
        axis.set_title(ticker.ticker_name, y=0.85, loc='left')
        axis.set_ylabel(f'{ticker.currency}')
        axis.tick_params(axis='x', labelrotation=45, labelsize=8)
        i = i+1

    fig.tight_layout(pad=0.5)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    return base64.b64encode(buf.getbuffer()).decode("ascii")


def draw_learning_rate(schedule, title, iterations=150):
    fig = Figure(figsize=(6, 2.5), dpi=75)
    axis = fig.add_subplot(1, 1, 1)

    axis.plot(
        [i+1 for i in range(iterations)],
        [schedule(i) for i in range(iterations)]
    )

    axis.grid(True)
    axis.autoscale_view()
    axis.set_title(title)
    axis.set_xlabel("Epoch")
    axis.set_ylabel("Learning Rate")

    buf = BytesIO()
    fig.savefig(buf, format="png")
    return base64.b64encode(buf.getbuffer()).decode("ascii")


def draw_losses(model_history):
    fig = Figure(figsize=(6, 3), dpi=200)
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(model_history.history['loss'], label='train')
    axis.plot(model_history.history['val_loss'], label='test')
    axis.set_title('Training Error')

    if model_history.history['loss'] == 'mae':
        axis.set_ylabel('Mean Absolute Error (MAE)', fontsize=10)
    else:
        axis.set_ylabel('Model Loss', fontsize=8)
        axis.set_xlabel('# Epochs', fontsize=8)

    axis.legend()
    axis.grid(b=True)
    axis.autoscale_view()
    fig.tight_layout(pad=0.5)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    return base64.b64encode(buf.getbuffer()).decode("ascii")


def draw_prediction(model, last_i, pred_range, r_scale, X_news, Y_news, LSTM_input):
    fig = Figure(figsize=(6, 3), dpi=200)
    axis = fig.add_subplot(1, 1, 1)

    prediction = (model.predict(LSTM_input) + 1) * r_scale

    axis.plot(X_news.index, Y_news, label='Present')

    axis.plot(
        [
            x for x in range(last_i + 1, last_i + pred_range + 1)
        ],
        prediction[0], label='Prediction')

    axis.legend()
    axis.grid(b=True)
    axis.autoscale_view()
    fig.tight_layout(pad=0.5)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    return base64.b64encode(buf.getbuffer()).decode("ascii")


def draw_test_prediction(
    df_original, model, window_len, LSTM_x_df_test_frames,
    y_df, LSTM_y_df_test_frames, stock, pred_range, nrows_training
):
    fig = Figure(figsize=(6, 3), dpi=200)
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(
        df_original.iloc[y_df[nrows_training:].index]['Fecha'],
        df_original.iloc[y_df[nrows_training:].index][stock], label='Actual'
    )

    LSTM_y_df_predict_frames = model.predict(LSTM_x_df_test_frames)

    step = window_len  # + pred_range
    for i in range(0, LSTM_y_df_predict_frames.shape[0], step):
        y_preds = []
        for y_pred in LSTM_y_df_predict_frames[i]:
            y_preds.append(
                y_df[i + nrows_training] * (y_pred + 1)
            )

        axis.plot(
            df_original.iloc[y_df[i+nrows_training:i+nrows_training+pred_range].index]['Fecha'],
            np.array(y_preds),
            label=f'Predicted {pred_range} days'
        )

    axis.set_title('Test Set: Prediction', fontsize=10)
    axis.tick_params(axis='x', labelrotation=45, labelsize=8)
    axis.set_ylabel(f'{stock}', fontsize=8)
    # axis.legend(prop={'size': 9})
    axis.grid(b=True)
    axis.autoscale_view()
    fig.tight_layout(pad=0.5)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    return base64.b64encode(buf.getbuffer()).decode("ascii")


def draw_single_timepoint_prediction(df_original, model, window_len,
                                     LSTM_test_inputs, test_set, stock):
    fig = Figure(figsize=(6, 3), dpi=200)
    axis = fig.add_subplot(1, 1, 1)
    axis.plot(
        [
            df_original.loc[ipos, 'Fecha']
            for ipos in test_set.index[window_len:]
        ],
        test_set[stock][window_len:], label='Actual'
    )

    axis.plot(
        [
            df_original.loc[ipos, 'Fecha']
            for ipos in test_set.index[window_len:]
        ],
        (
            (np.transpose(model.predict(LSTM_test_inputs))+1) *
            test_set[stock].values[:-window_len]
        )[0],
        label='Predicted'
    )

    axis.annotate('MAE: %.4f' % np.mean(
        np.abs((np.transpose(
            model.predict(LSTM_test_inputs)
        )+1)-(
            test_set[stock].values[window_len:]
        )/(test_set[stock].values[:-window_len]))
    ),
        xy=(0.75, 0.9),
        xycoords='axes fraction',
        xytext=(0.75, 0.9),
        textcoords='axes fraction')

    axis.set_title('Test Set: Single Timepoint Prediction', fontsize=10)
    axis.tick_params(axis='x', labelrotation=45, labelsize=8)
    axis.set_ylabel(f'{stock}', fontsize=8)
    axis.legend(prop={'size': 9})
    axis.grid(b=True)
    axis.autoscale_view()
    fig.tight_layout(pad=0.5)

    buf = BytesIO()
    fig.savefig(buf, format="png")
    return base64.b64encode(buf.getbuffer()).decode("ascii")
