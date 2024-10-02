import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt  # Import matplotlib.pyplot


def plot_candlesticks_mpl(comparison_df):
    comparison_df['Start Time'] = pd.to_datetime(comparison_df['Start Time'])

    actual_data = comparison_df[['Start Time', 'Open Actual', 'High Actual', 'Low Actual', 'Close Actual']].set_index('Start Time')
    predicted_data = comparison_df[['Start Time', 'Open Predicted', 'High Predicted', 'Low Predicted', 'Close Predicted']].set_index('Start Time')

    actual_data.columns = ['Open', 'High', 'Low', 'Close']
    predicted_data.columns = ['Open', 'High', 'Low', 'Close']

    # Create a figure for actual data
    plt.figure(figsize=(12, 6))
    mpf.plot(actual_data, type='candle', style='charles',
             title='Actual OHLC Candlestick Chart', ylabel='Price',
             volume=False, mav=(3, 6), show_nontrading=True)
    plt.show()  # Display the actual data plot

    # Create a new figure for predicted data
    plt.figure(figsize=(12, 6))
    mpf.plot(predicted_data, type='candle', style='charles',
             title='Predicted OHLC Candlestick Chart', ylabel='Price',
             volume=False, mav=(3, 6), show_nontrading=True)
    plt.show()  # Display the predicted data plot


