from dataPreparation.klineData_processing import kline_data_processing
from EDA.candleStickChart import plot_candlestick
from XGBoost.dataSplit import split_kline_data
from XGBoost.prepareData import prepare_data
from XGBoost.trainXGBoost import train_xgboost
from XGBoost.candleStickCompare import plot_candlesticks_mpl

kline_data_processing()
plot_candlestick()
train_data, test_data= split_kline_data()
X_train, y_train, X_test, y_test=prepare_data(train_data, test_data)
comparison_df=train_xgboost(X_train, y_train, X_test, y_test, test_data)
plot_candlesticks_mpl(comparison_df)
