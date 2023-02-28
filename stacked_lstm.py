import streamlit as st
from datetime import date
import plotly.express as px
import yfinance as yf
import matplotlib.pyplot as plt
from plotly import graph_objs as go
import numpy as np
import numpy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from streamlit_option_menu import option_menu

import datetime as dt
selected=option_menu(
        menu_title='Stock Market Prediction',
        options= ['About','Application'],
        icons=['briefcase-fill','hourglass-split'],
        default_index=0,
        orientation='horizontal',
        styles={
        "container": {"padding": "0!important", "background-color": "grey"},
        "icon": {"color": "black", "font-size": "30px"}, 
        "nav-link": {"font-size": "20px", "text-align": "left", "margin":"0px", "--hover-color": "white"},
        "nav-link-selected": {"background-color": "#13A88A"},
    }
    )
data=pd.read_csv('stock.csv')
data.dropna(inplace=True)
START=  dt.date(2021, 1, 1)
END =  dt.datetime.today()

@st.cache_data
def load_data(ticker):
    data = yf.download(ticker, START, END)
    data.reset_index(inplace=True)
    return data

if selected=='About':
    taba, tabc = st.tabs(["Introduction","Procedure"])
    with taba:
        st.title('Stock Makert Prediction.')
        st.header('Please Note: The streamlit app is created just for educational purpose.')
        st.write('-    Stock market prediction using stacked LSTM is a popular application of deep learning in finance..Several LSTM layers make up a stacked LSTM model, a kind of recurrent neural network (RNN). A series of historical stock market data, including daily stock prices, trading volume serves as the input of the model.The output is a forecast of future stock price movement.')
        st.write('-    The stacked LSTM model employs a number of levels of LSTM cells, each layer made up of a number of LSTM units. The first layer of the model receives the input data, while the subsequent layers receive the output of the previous layer as input. When each layer can capture more abstract and high-level representations of the input, the model is able to learn increasingly complicated patterns in the input data.')
        st.write('-    Once trained, the model can be used to make predictions based on fresh, unused data. A series of historical data are used as the input, and its output is a forecast of how the stock price will move in the future. To assess the accuracy, the projected values and the actual values can be compared.')
        st.write('-    In conclusion, a stacked LSTM model is an effective tool for stock market forecasting because it can recognise intricate patterns in historical data and predict future stock price movements with precision. We can create a trustworthy stock market prediction system that can be utilised for investment and trading decisions by training the model on historical data and assessing its performance on a test set.')
        st.write('-    It is crucial to remember that there is no assurance that stock market predictions will be accurate, even if they might be valuable for making wise financial decisions. The stock market is complicated and affected by a variety of unpredictable circumstances, such as world events, political unrest, and natural disasters.')

    with tabc:
        st.header('Steps Involved.')
        st.write('-    A text input is created for entering your desired stock symbol(PS: CASE SENSITIVE).')
        st.write('-    Data retreived from yfinance library ranging from 1st January 2021 till today.')
        st.write('-    Plotting of graphs which includes:')
        st.write('--    **Candlestick charts**')
        st.write('--    **Line chart to plot the trend in close price.**')
        st.write('--    **Box and Whisker Chart**')
        st.write('--    **Plot to check the trend in differences between close and open price**')
        st.write('-    As the motive of the project is to predict close price for the next 30 days, the close price is split in to training and testing data.')
        st.write('-    The training and testing data is now used to for performing a STACKED LSTM with a timestep ==100.')
        st.write('-    A while loop is created for prediction of the stock price for the next 30 days.')
        st.write('-    Prediction Process approximate time: 30 seconds.')
try:
        
        if selected=='Application':
                data=pd.read_csv('stock.csv')
                data.dropna(inplace=True)
#                 selected_stock = st.text_input('Enter your stock')
#                 selected_stock1=selected_stock.upper()
#                 df = load_data(selected_stock1)
#                 stock_name = data.loc[data['Symbol'].str.upper() == selected_stock, 'Name'].values[0]
#         if selected_stock1 in data['Symbol'].str.upper().values:
#                 stock_name = data.loc[data['Symbol'].str.upper() == selected_stock1, 'Name'].values[0]
#                 st.header(f'The name of the stock with symbol {selected_stock1} is {stock_name}.')
#         else:
#                 st.write(f'Stock symbol {selected_stock} not found.')
        tab2, tab3,tab4 = st.tabs(["Data-set", "Data Visualization", "Predictions"])
        with tab2:
            selected_stock = st.text_input('Enter your stock')
            selected_stock1=selected_stock.upper()
            df = load_data(selected_stock1)
            if st.button("Submit"):
                        stock_name = data.loc[data['Symbol'].str.upper() == selected_stock, 'Name'].values[0]
                        if selected_stock1 in data['Symbol'].str.upper().values:
                                stock_name = data.loc[data['Symbol'].str.upper() == selected_stock1, 'Name'].values[0]
                                st.header(f'The name of the stock with symbol {selected_stock1} is {stock_name}.')
                                st.write("You have entered", selected_stock)
                                st.experimental_data_editor(df)  
                                data_load_state.text('Loading data... done!')
                        else:
                                st.write(f'Stock symbol {selected_stock} not found.')
            
#             data_load_state = st.text('Loading data...')
#             st.write("You have entered", selected_stock)
#             st.experimental_data_editor(df)  
#             data_load_state.text('Loading data... done!')


        df1=df.copy()
        df1['Difference']=df1['Close']-df1['Open']

        fig = go.Figure(data=[go.Candlestick(x=df["Date"],
                            open=df["Open"],
                            high=df["High"],
                            low=df["Low"],
                            close=df["Close"])])
        fig.update_layout(
                    title='Candlestick Chart',
                    yaxis_title='Price',
                    xaxis_rangeslider_visible=True)

        fig2=px.line(df, x="Date", y="Close", title='Trend of Closing price')
        fig2.update_xaxes(rangeslider_visible=True,rangeselector=dict(buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")])))
        fig3 = px.box(df, x=df['Date'].dt.year, y='Close', points='all', title='Box and Whisker Chart')

        fig4=px.line(df, x="Date", y="Volume", title='Trend in Volume')
        fig4.update_xaxes(rangeslider_visible=True,rangeselector=dict(buttons=list([
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")])))

        with tab3:
            st.plotly_chart(fig,use_container_width=True,renderer='webgl')
            st.plotly_chart(fig2,use_container_width=True,renderer='webgl')
            st.plotly_chart(fig3,use_container_width=True,renderer='webgl')
            st.plotly_chart(fig4,use_container_width=True,renderer='webgl')

        df1=df.reset_index()['Close']
        scaler=MinMaxScaler(feature_range=(0,1))
        df1=scaler.fit_transform(np.array(df1).reshape(-1,1))

        training_size=int(len(df1)*0.7)
        test_size=len(df1)-training_size
        train_data,test_data=df1[0:training_size,:],df1[training_size:len(df1),:1]

        import numpy
        def create_dataset(dataset, time_step=1):
            dataX, dataY = [], []
            for i in range(len(dataset)-time_step-1):
                a = dataset[i:(i+time_step), 0] 
                dataX.append(a)
                dataY.append(dataset[i + time_step, 0])
            return numpy.array(dataX), numpy.array(dataY)

        time_step = 100
        X_train, y_train = create_dataset(train_data, time_step)
        X_test, ytest = create_dataset(test_data, time_step)

        X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)
        X_test = X_test.reshape(X_test.shape[0],X_test.shape[1] , 1)


        with tab4:
            model=Sequential()
            model.add(LSTM(50,return_sequences=True,input_shape=(100,1)))
            model.add(LSTM(50,return_sequences=True))
            model.add(LSTM(50))
            model.add(Dense(1))
            model.compile(loss='mean_squared_error',optimizer='adam')

            model.fit(X_train,y_train,validation_data=(X_test,ytest),epochs=20,batch_size=64,verbose=1)
            train_predict=model.predict(X_train)
            test_predict=model.predict(X_test)

            train_predict=scaler.inverse_transform(train_predict)
            test_predict=scaler.inverse_transform(test_predict)



            x_input=test_data[len(test_data)-100:].reshape(1,-1)
            temp_input=list(x_input)
            temp_input=temp_input[0].tolist()

            lst_output=[]
            n_steps=100
            i=0
            while(i<31):
                if(len(temp_input)>100):
                    x_input=np.array(temp_input[1:])
                    x_input=x_input.reshape(1,-1)
                    x_input = x_input.reshape((1, n_steps, 1))
                    yhat = model.predict(x_input, verbose=0)
                    st.write("For Day {}, the predicted output is {}".format(i,scaler.inverse_transform(yhat)))
                    temp_input.extend(yhat[0].tolist())
                    temp_input=temp_input[1:]
                    lst_output.extend(yhat.tolist())
                    i=i+1
                else:
                    x_input = x_input.reshape((1, n_steps,1))
                    yhat = model.predict(x_input, verbose=0)
                    temp_input.extend(yhat[0].tolist())
                    lst_output.extend(yhat.tolist())
                    i=i+1

except:
    pass
