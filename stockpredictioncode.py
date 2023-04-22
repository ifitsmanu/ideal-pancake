
import numpy as np
import yfinance as yf
import math
import argparse
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from keras.models import Sequential
from keras.layers import Dense, LSTM
from sklearn.preprocessing import MinMaxScaler


def prepare_data(stock_symbol, start_date='2012-01-01'):
    today = datetime.today().strftime('%Y-%m-%d')
    df = yf.download(stock_symbol, start=start_date, end=today)
    data = df.filter(['Close'])
    dataset = data.values
    training_data_len = math.ceil(len(dataset) * .8)
    scale = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scale.fit_transform(dataset)
    return scaled_data, training_data_len, scale, data


def create_training_data(scaled_data, training_data_len):
    train_data = scaled_data[0:training_data_len, :]
    X_train = []
    y_train = []
    for i in range(60, len(train_data)):
        X_train.append(train_data[i-60:i, 0])
        y_train.append(train_data[i, 0])
    X_train, y_train = np.array(X_train), np.array(y_train)
    X_train = np.reshape(X_train, (X_train.shape[0], X_train.shape[1], 1))
    return X_train, y_train


def build_and_train_rnn(X_train, y_train, epochs=10, batch_size=32):
    regressor = Sequential()
    regressor.add(LSTM(units=50, return_sequences=True, input_shape=(X_train.shape[1], 1)))
    regressor.add(LSTM(units=50, return_sequences=False))
    regressor.add(Dense(units=25))
    regressor.add(Dense(units=1))
    regressor.compile(optimizer='adam', loss='mean_squared_error')
    regressor.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)
    return regressor


def predict_tomorrow_stock(stock_symbol, regressor, scale, start_date='2012-01-01'):
    today = datetime.today().strftime('%Y-%m-%d')
    quote = yf.download(stock_symbol, start=start_date, end=today)
    new_df = quote.filter(['Close'])
    last_60_days = new_df[-60:].values
    last_60_days_scaled = scale.transform(last_60_days)
    x_test = []
    x_test.append(last_60_days_scaled)
    x_test = np.array(x_test)
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    pred_price = regressor.predict(x_test)
    pred_price = scale.inverse_transform(pred_price)
    return pred_price


def visualize_predictions(data, training_data_len, stock_symbol):
    train = data[:training_data_len]
    valid = data[training_data_len:]
    valid['Predictions'] = predictions
    plt.figure(figsize=(16, 8))
    plt.title(f'Model Predictions vs Actual Prices for {stock_symbol}')
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Close Price USD ($)', fontsize=18)
    plt.plot(train['Close'])
    plt.plot(valid[['Close', 'Predictions']])
    plt.legend(['Train', 'Actual', 'Predictions'], loc='lower right')
    plt.show()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Predict stock prices using RNN')
    parser.add_argument('stock_symbol', type=str, help='Stock symbol of the company (e.g., AAPL)')
    parser.add_argument('--epochs', type=int, default=10, help='Number of epochs for training the model')
    parser.add_argument('--batch_size', type=int, default=32, help='Batch size for training the model')
    args = parser.parse_args()

    stock_symbol = args.stock_symbol
    epochs = args.epochs
    batch_size = args.batch_size

    scaled_data, training_data_len, scale, data = prepare_data(stock_symbol)
    X_train, y_train = create_training_data(scaled_data, training_data_len)
    regressor = build_and_train_rnn(X_train, y_train, epochs=epochs, batch_size=batch_size)
    pred_price = predict_tomorrow_stock(stock_symbol, regressor, scale)
    print(f'Tomorrows stock price for {stock_symbol} is: {pred_price[0][0]}')

    # Predict prices for validation data (data not used in training)
    valid_data = scaled_data[training_data_len - 60:, :]
    X_valid = []
    for i in range(60, len(valid_data)):
        X_valid.append(valid_data[i - 60:i, 0])
    X_valid = np.array(X_valid)
    X_valid = np.reshape(X_valid, (X_valid.shape[0], X_valid.shape[1], 1))
    predictions = regressor.predict(X_valid)
    predictions = scale.inverse_transform(predictions)

    # Visualize the model's predictions against actual prices
    visualize_predictions(data, training_data_len, stock_symbol)










