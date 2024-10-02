# Function to load and prepare data
def prepare_data(train_data, test_data):
    """
    Load the training and testing datasets and prepare the features and target variables.

    Parameters:
    - train_data: df, training data
    - test_data: df, testing data

    Returns:
    - tuple: (X_train, y_train), (X_test, y_test)
    """

    # Prepare features and targets
    X_train = train_data[['high', 'low', 'close', 'volume']]
    y_train = train_data[['open', 'high', 'low', 'close']]

    X_test = test_data[['high', 'low', 'close', 'volume']]
    y_test = test_data[['open', 'high', 'low', 'close']]

    return X_train, y_train, X_test, y_test


