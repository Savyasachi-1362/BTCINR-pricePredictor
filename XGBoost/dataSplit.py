import pandas as pd
import os
def split_kline_data(train_size=1400, test_size=100):
    """
    Load Kline data from a CSV file, check if it contains enough rows, and split it into training and testing sets.

    Args:
        train_size (int): Number of rows to use for the training set, with a default of 1400.
        test_size (int): Number of rows to use for the testing set, with a default of 100.
        save_to_csv (bool): If True, save the training and testing datasets to new CSV files (default is False).

    Returns:
        tuple: Two DataFrames containing the training and testing data.
    """
    # Load the Kline data from the CSV file
    df_kline = pd.read_csv("D:\Varun\PythonFiles\Pi 42 - Copy\dataPreparation\kline_data.csv")

    # Check if the dataset contains enough rows
    if len(df_kline) < (train_size + test_size):
        raise ValueError(f"The dataset should contain at least {train_size + test_size} rows.")

    # Split the data into training and testing sets
    train_data = df_kline.iloc[:train_size]  # First `train_size` rows for training
    test_data = df_kline.iloc[train_size:train_size + test_size]  # Next `test_size` rows for testing

    # Output the shapes of the resulting DataFrames
    print("Training data shape:", train_data.shape)
    print("Testing data shape:", test_data.shape)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    train_csv_path = os.path.join(script_dir, 'kline_train_data.csv')
    test_csv_path= os.path.join(script_dir, 'kline_test_data.csv')
    train_data.to_csv(train_csv_path, index=False)
    test_data.to_csv(test_csv_path, index=False)
    print("Training and testing data saved to 'kline_train_data.csv' and 'kline_test_data.csv'.")
    return train_data, test_data

