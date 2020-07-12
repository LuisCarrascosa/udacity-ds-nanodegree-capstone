import base64
from io import BytesIO
from matplotlib.figure import Figure


def drawFeatures_byDict(df, nrows, ncols, tickers, f_ini=None, f_fin=None):
    # Generate the figure **without using pyplot**.
    # print(f'nrows: {nrows}, ncols: {ncols}')
    # print(f'f_ini: {f_ini}, f_fin: {f_fin}')
    # [9, 4] 2 graficas
    # [9, 8] 3
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
        axis.set_title(ticker.ticker_name)
        axis.set_ylabel(f'{ticker.currency}')
        axis.tick_params(axis='x', labelrotation=45, labelsize=8)
        i = i+1

    fig.tight_layout(pad=3.0)

    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
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
    # Embed the result in the html output.
    return base64.b64encode(buf.getbuffer()).decode("ascii")
