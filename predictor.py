import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pandas_datareader as web
import math
import robin_stocks.robinhood as r
import pyotp
import sys
import datetime as dt

from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, LSTM


# Data retrieval
company = 'fb'
start = dt.datetime(2012,1,1)
end = dt.datetime(2020,1,1)
data = web.DataReader(company, 'yahoo', start, end)

print(data)

# Data processing
scalar = MinMaxScaler(feature_range=(0,1))
scaled_data = scalar.fit_transform(data['Close'].values.reshape(-1,1)) 

# print(scaled_data)

prediction_days = 60

x_train = []
y_train = []

for x in range(prediction_days, len(scaled_data)):
    x_train.append(scaled_data[x - prediction_days:x, 0])
    y_train.append(scaled_data[x, 0])

x_train, y_train = np.array(x_train), np.array(y_train)
x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

# Build Model
model = Sequential()

model.add(LSTM(units=50, return_sequences=True, input_shape=(x_train.shape[1], 1)))
model.add(Dropout(0.2))
model.add(LSTM(units=50, return_sequences=True))
model.add(Dropout(0.2))
model.add(LSTM(units=50))
model.add(Dropout(0.2))
model.add(Dense(units=1)) # Final layer, ouputs prediction

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train, y_train, epochs=25, batch_size=32)

# Test model accuracy
test_start = dt.datetime(2020, 1, 1)
test_end = dt.datetime.now()
test_data = web.DataReader(company, 'yahoo', test_start, test_end)
actual_price = test_data['Close'].values

total_dataset = pd.concat((data['Close'], test_data['Close']), axis=0)

model_inputs = total_dataset[len(total_dataset) - len(test_data) - prediction_days:].values
model_inputs = model_inputs.reshape(-1,1)
model_inputs = scalar.transform(model_inputs)

# Make test predictions

# Robinhood trading
totp = pyotp.TOTP("GTGBTO63C46YCH65").now()
login = r.login(pickle.load(open(username, 'rb')), pickle.load(open(password, 'rb')), mfa_code=totp) 