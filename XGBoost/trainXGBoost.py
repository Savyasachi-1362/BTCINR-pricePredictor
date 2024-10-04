from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import pandas as pd
import os


def train_xgboost(X_train, y_train, X_test, y_test, test_data):
    """
    Train and evaluate XGBoost models for OHLC.

    Parameters:
    - X_train: Training features
    - y_train: Training target values
    - X_test: Test data features
    - y_test: Test data target values
    - test_data: Original test dataset (to include timestamps and volume in the output)

    Returns:
    - comparison_df: DataFrame with actual and predicted values for all target variables
    """
    # Initialize the XGBoost model
    model = XGBRegressor(random_state=42)

    # Set up the parameter grid for GridSearchCV
    param_grid = {
        'n_estimators': [50, 100, 150, 200],
        'learning_rate': [0.01, 0.1, 0.2],
        'max_depth': [3, 5, 7],
        'min_child_weight': [1, 3, 5],
    }

    # Initialize GridSearchCV
    grid_search = GridSearchCV(estimator=model,
                               param_grid=param_grid,
                               scoring='neg_mean_squared_error',
                               cv=5,  # 5-fold cross-validation
                               verbose=1,
                               n_jobs=-1)  # Use all available cores

    # Fit GridSearchCV to find the best parameters for 'open'
    grid_search.fit(X_train, y_train['open'])
    best_params = grid_search.best_params_
    print("Best Parameters for 'open':", best_params)
    model_open = grid_search.best_estimator_
    open_pred = model_open.predict(X_test)
    '''
    Here, we are performing the grid search only for open beacuse all 4 metrics, open, high, low, close are correlated and
    performing 4 grid searches is computationally expensive.

    Using the best params for open for all 4 cases gave much better results (lower RMSE and MAE) than when using 4 different 
    sets of params. 
    '''

    #Configure GridSearchCV for 'high'
    model_high = XGBRegressor(random_state=42, **grid_search.best_params_)
    model_high.fit(X_train, y_train['high'])
    high_pred = model_high.predict(X_test)

    # Configure GridSearchCV for 'low'
    model_low = XGBRegressor(random_state=42, **grid_search.best_params_)
    model_low.fit(X_train, y_train['low'])
    low_pred = model_low.predict(X_test)

    # For 'close'
    model_close = XGBRegressor(random_state=42, **grid_search.best_params_)
    model_close.fit(X_train, y_train['close'])
    close_pred = model_close.predict(X_test)

   #df for side by side Comparison
    comparison_df = pd.DataFrame({
        'Start Time': test_data['startTime'],
        'End Time': test_data['endTime'],
        'Volume': X_test['volume'],
        'Open Actual': y_test['open'],
        'Open Predicted': open_pred,
        'High Actual': y_test['high'],
        'High Predicted': high_pred,
        'Low Actual': y_test['low'],
        'Low Predicted': low_pred,
        'Close Actual': y_test['close'],
        'Close Predicted': close_pred
    })
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'kline_comparison_with_timestamps.csv')
    comparison_df.to_csv(csv_path, index=False)
    print("Comparison saved to 'kline_comparison_with_timestamps.csv'.")

    def calculate_error_metrics(y_true, y_pred, target_name):
        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        print(f"{target_name} - Mean Absolute Error: {mae}")
        print(f"{target_name} - Root Mean Squared Error: {rmse}")

    calculate_error_metrics(y_test['open'], open_pred, 'Open')
    calculate_error_metrics(y_test['high'], high_pred, 'High')
    calculate_error_metrics(y_test['low'], low_pred, 'Low')
    calculate_error_metrics(y_test['close'], close_pred, 'Close')

    return comparison_df


