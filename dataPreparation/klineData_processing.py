import requests
from constants import BASE_URL, TRADING_PAIR
import pandas as pd
import os
def kline_data_processing(interval='5m', limit=8000):  # default parameters being 5 minutes and 8000 candles
    try:
        pair = TRADING_PAIR
        params = {
            'pair': pair,
            'interval': interval,
            'limit': limit
        }
        headers = {
            'Content-Type': 'application/json'
        }
        kline_url = f"{BASE_URL}market/klines"
        response = requests.post(kline_url, json=params, headers=headers)
        response.raise_for_status()  # Raises an error for 4xx/5xx responses
        response_data = response.json()

        if response_data:
            df_kline = pd.DataFrame(response_data)
            df_kline.columns = ['startTime', 'open', 'high', 'low', 'close', 'endTime', 'volume']
            df_kline['startTime'] = pd.to_datetime(df_kline['startTime'], unit='ms')
            df_kline['endTime'] = pd.to_datetime(df_kline['endTime'], unit='ms')
            df_kline['startTime'] = df_kline['startTime'].dt.strftime('%Y-%m-%d %H:%M:%S')
            df_kline['endTime'] = df_kline['endTime'].dt.strftime('%Y-%m-%d %H:%M:%S') #converting the times to Date and Time format
            df_kline['open'] = pd.to_numeric(df_kline['open'])
            df_kline['high'] = pd.to_numeric(df_kline['high'])
            df_kline['low'] = pd.to_numeric(df_kline['low'])
            df_kline['close'] = pd.to_numeric(df_kline['close'])
            df_kline['volume'] = pd.to_numeric(df_kline['volume'])
            try:
                script_dir = os.path.dirname(os.path.abspath(__file__))
                csv_path = os.path.join(script_dir, 'kline_data.csv')
                df_kline.to_csv(csv_path, index=False)
            except Exception as e:
                print(f"Error saving CSV: {e}")
        else:
            print("No data returned from the API.")
    except ValueError:
        print("Please enter valid inputs for interval.")
    except requests.exceptions.HTTPError as err:
        print(f"Error: {err.response.text if err.response else err}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None
