# trading/strategies.py
import pandas as pd
import talib

def apply_strategy(df, strategy_name):
    if strategy_name == 'moving_average_crossover':
        return moving_average_crossover_strategy(df)
    elif strategy_name == 'rsi':
        return rsi_strategy(df)
    # Add more strategies as needed
    else:
        raise ValueError(f"Unknown strategy: {strategy_name}")

def moving_average_crossover_strategy(df, short_window=5, long_window=20):
    df['Short_MA'] = df['Close'].rolling(window=short_window).mean()
    df['Long_MA'] = df['Close'].rolling(window=long_window).mean()
    df['Signal'] = 0

    # Generate signals based on moving average crossovers
    df.loc[df['Short_MA'] > df['Long_MA'], 'Signal'] = 1
    df.loc[df['Short_MA'] < df['Long_MA'], 'Signal'] = -1

    return df

def rsi_strategy(df, rsi_period=14, overbought_threshold=70, oversold_threshold=30):
    df['RSI'] = talib.RSI(df['Close'], timeperiod=rsi_period)
    df['Signal'] = 0

    # Generate signals based on RSI levels
    df.loc[df['RSI'] > overbought_threshold, 'Signal'] = -1
    df.loc[df['RSI'] < oversold_threshold, 'Signal'] = 1

    return df
