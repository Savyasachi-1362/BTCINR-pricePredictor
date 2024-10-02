import pandas as pd
import pandas_ta as ta
import mplfinance as mpf
import matplotlib.pyplot as plt
import os

def plot_candlestick():
    """
    Reads Kline data from CSV, processes columns, calculates RSI, MA, and EWMA.
    Plots a candlestick chart with Bollinger Bands, and saves RSI, MA, and EWMA data to 'RSI&MA.csv' in the same directory.
    """
    csv_file = r'D:\Varun\PythonFiles\Pi 42 - Copy\dataPreparation\kline_data.csv'

    if not os.path.exists(csv_file):
        print(f"The csv file '{csv_file}' does not exist.")
        return
    df_kline = pd.read_csv(csv_file)
    df_kline.columns = ['startTime', 'open', 'high', 'low', 'close', 'endTime', 'volume']
    df_kline['startTime'] = pd.to_datetime(df_kline['startTime'], format='%Y-%m-%d %H:%M:%S')

    df_kline.set_index('startTime', inplace=True)
    df_kline[['open', 'high', 'low', 'close', 'volume']] = df_kline[['open', 'high', 'low', 'close', 'volume']].apply(pd.to_numeric)
    if df_kline.isnull().values.any():
        df_kline.dropna(inplace=True)

    # Calculating RSI
    df_kline['RSI'] = ta.rsi(df_kline['close'], length=14)

    # Calculating SMA
    df_kline['SMA10'] = ta.sma(df_kline['close'], length=10)
    df_kline['SMA14'] = ta.sma(df_kline['close'], length=14)

    # Calculate EWMA
    df_kline['EWMA'] = df_kline['close'].ewm(span=20, adjust=False).mean()

    # Specifying the candlestick chart attributes
    mc = mpf.make_marketcolors(up='g', down='r', edge='i', wick='i', volume='in')
    s = mpf.make_mpf_style(base_mpf_style='yahoo', marketcolors=mc)

    bbands = ta.bbands(df_kline['close'], length=20, std=2)
    df_kline['BBL'] = bbands['BBL_20_2.0']  # Lower band
    df_kline['BBM'] = bbands['BBM_20_2.0']  # Middle band (SMA)
    df_kline['BBU'] = bbands['BBU_20_2.0']  # Upper band

    ap = [
        mpf.make_addplot(df_kline['BBL'], color='blue'),  # Lower Bollinger Band
        mpf.make_addplot(df_kline['BBM'], color='purple'),  # Middle Bollinger Band
        mpf.make_addplot(df_kline['BBU'], color='blue')  # Upper Bollinger Band
    ]
    mpf.plot(df_kline, type='candle', style=s, addplot=ap, volume=True,
             title='Candlestick Chart with Bollinger Bands', ylabel='Price')

    #Plotting the RSI
    plt.figure(figsize=(10, 5))
    plt.plot(df_kline['RSI'], label='RSI', color='orange')
    plt.axhline(70, linestyle='--', alpha=0.5, color='red')
    plt.axhline(30, linestyle='--', alpha=0.5, color='green')
    plt.title('Relative Strength Index (RSI)')
    plt.xlabel('Time')
    plt.ylabel('RSI Value')
    plt.legend()
    plt.grid()

    #Plotting EWMA
    plt.figure(figsize=(10, 5))
    plt.plot(df_kline['EWMA'], label='EWMA', color='blue')
    plt.plot(df_kline['SMA10'],label='SMA10',color='red')
    plt.plot(df_kline['SMA14'], label='SMA14', color='green')
    plt.title('Exponentially Weighted Moving Average (EWMA)')
    plt.xlabel('Time')
    plt.ylabel('EWMA Value')
    plt.legend()
    plt.grid()
    plt.show()

    script_dir = os.path.dirname(os.path.abspath(__file__))
    rsi_ma_csv_path = os.path.join(script_dir, 'RSI&MA.csv')
    df_kline[['RSI', 'SMA10','SMA14', 'EWMA']].dropna().to_csv(rsi_ma_csv_path, index=True)
# Call the function
plot_candlestick()
