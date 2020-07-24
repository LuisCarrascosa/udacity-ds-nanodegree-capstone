def get_ti_keys():
    return ['ma7', 'ma21', '26ema', '12ema', 'MACD', '20sd',
            'upper_band', 'lower_band', 'ema', 'momentum']


def get_technical_indicators(df, column):
    # Create 7 and 21 days Moving Average
    df['ma7'] = df[column].rolling(window=7).mean()
    df['ma21'] = df[column].rolling(window=21).mean()

    # Moving Average Convergence Divergence (MACD)
    df['26ema'] = df[column].ewm(adjust=False, span=26).mean()
    df['12ema'] = df[column].ewm(adjust=False, span=12).mean()
    df['MACD'] = (df['12ema'] - df['26ema'])

    # Create Bollinger Bands
    df['20sd'] = df[column].rolling(window=20).std()
    df['upper_band'] = df['ma21'] + (df['20sd']*2)
    df['lower_band'] = df['ma21'] - (df['20sd']*2)

    # Create Exponential moving average
    df['ema'] = df[column].ewm(com=0.5).mean()

    # Create Momentum
    df['momentum'] = df[column]-1

    return df
