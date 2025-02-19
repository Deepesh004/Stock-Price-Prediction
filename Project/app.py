import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from keras.models import load_model
import streamlit as st

# Set the deprecation option to hide the warning
st.set_option('deprecation.showPyplotGlobalUse', False)

start_date = "2010-01-01"
end_date = "2021-09-01"

st.title("Stock Trend Prediction")
user_input = st.text_input("Enter Stock Ticker", "AAPL")

# Fetch data using yfinance
df = yf.download(user_input, start=start_date, end=end_date)

st.subheader("Data from 2010-2019")
st.write(df.describe())

st.subheader("Closing Price vs Time Chart ")
fig, ax = plt.subplots()  # Create a figure and axis object
ax.plot(df.Close)
st.pyplot(fig)

st.subheader("Closing Price vs Time Chart with 100MA")
ma100 = df.Close.rolling(100).mean()
fig, ax = plt.subplots()
ax.plot(ma100)
ax.plot(df.Close)
st.pyplot(fig)

st.subheader("Closing Price vs Time Chart with 100MA & 200MA")
ma100 = df.Close.rolling(100).mean()
ma200 = df.Close.rolling(200).mean()
fig, ax = plt.subplots()
ax.plot(ma100, 'r')
ax.plot(ma200, 'g')
ax.plot(df.Close, 'b')
st.pyplot(fig)


data_training = pd.DataFrame(df['Close'][0:int(len(df)*0.70)])
data_testing = pd.DataFrame(df['Close'][int(len(df)*0.70):int(len(df))])

from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler(feature_range=(0,1))

data_training_array = scaler.fit_transform(data_training)

x_train = []
y_train = []

for i in range(100,data_training_array.shape[0]):
    x_train.append(data_training_array[i-100:i])
    y_train.append(data_training_array[i,0])

x_train ,y_train = np.array(x_train),np.array(y_train)


model = load_model("Keras_model.h5")

past_100_days = data_training.tail(100)

final_df = pd.concat([past_100_days, data_testing], ignore_index=True)
input_data = scaler.fit_transform(final_df)

x_test =[]
y_test=[]

for i in range(100,input_data.shape[0]):
    x_test.append(input_data[i-100:i])
    y_test.append(input_data[i,0])

x_test,y_test=np.array(x_test),np.array(y_test)
y_predicted = model.predict(x_test)

scaler.scale_
scale_faxtor = 1/0.00850539
y_predicted = y_predicted*scale_faxtor
y_test= y_test * scale_faxtor

st.subheader("Prediction vs Original")
plt.figure(figsize=(12,6))
plt.plot(y_test,'b',label='Original Price')
plt.plot(y_predicted,'r',label='Predicted Price')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
st.pyplot() 
