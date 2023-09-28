import streamlit as st
import requests
from streamlit_lottie import st_lottie
import keras
import numpy as np
import pandas as pd
import sklearn

df=pd.read_csv("Dataset-1.csv")
X=df.iloc[:,:-1].values
from sklearn.preprocessing import MinMaxScaler
mms = MinMaxScaler()
x_m= mms.fit_transform(X)
# Scale the features using StandardScaler
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
x = scaler.fit_transform(x_m)


# Load the trained model
model = keras.models.load_model('model.h5')


# Define a function to make predictions
def make_prediction(nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall):
    # Create an input array for prediction
    input_data = [[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]]

    # Scale the input data
    input_data_scaled = mms.transform(input_data)
    input_data_scaled = scaler.transform(input_data_scaled)

    # Predict the yield value
    crop = model.predict(input_data_scaled)

    # Flatten the array into a 1D array
    crop_arr= crop.flatten()

    # Find the index of the maximum value in the predicted yield array
    max_index = int(np.argmax(crop_arr))

    cake = {
    'rice🌾': 0, 'maize🌽': 1, 'chickpea': 2, 'kidneybeans🫘': 3, 'pigeonpeas': 4,
    'mothbeans🫘': 5, 'mungbean🫘': 6, 'blackgram': 7, 'lentil': 8, 'pomegranate': 9,
    'banana🍌': 10, 'mango🥭': 11, 'grapes🍇': 12, 'watermelon🍉': 13, 'muskmelon🍈': 14,
    'apple🍎': 15, 'orange🍊': 16, 'papaya': 17, 'coconut🥥': 18, 'cotton': 19, 'jute': 20,
    'coffee': 21}

    # Function to get the string value for a given number
    def get_string_from_number(number):
        for key, value in cake.items():
            if value == number:
                return key
        return "Number not found in the dictionary."


    # Get the corresponding string value
    result = get_string_from_number(max_index)

    return result


st.set_page_config(page_title="Recommendation of crop",layout="wide")

def load_lottieurl(url):
    r=requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()


st.title("Recommendation Of Crop 🍀")


lottie_coding=load_lottieurl("https://lottie.host/8e0b2d84-9b97-4872-ab84-e50eef454d51/dn8exImHZP.json")
with st.container():
    st.write("---")
    left_column,right_column=st.columns(2)
    with left_column:
        st.header("About this website")
        st.write("""Recommendation of crop,this progect aims to recommend the best suitable crop for the given land based on various features like
                 -Nitrogen level in soil
                 -phosporous level in soil
                 -Potassium level in soil
                 -ph of the soil
                 -Average temperature 
                 -Humidity percentage""")
        st.header("  ")
        N=st.number_input("Enter the nitrogen value of the soil")
        P=st.number_input("Enter the phosporous value of the soil")
        K=st.number_input("Enter the potassium value of the soil")
        T=st.number_input("Enter the average temperature of this year")
        HUM=st.number_input("Enter the average humidity value ")
        ph=st.number_input("Enter the ph value of the soil")
        RF=st.number_input("Enter the average rainfall value of this year")
        st.header("Recommended crop")
         # Add a button to call the prediction function
        if st.button("Predict"):
            # Make a prediction
            result = make_prediction(N, P, K, T,HUM, ph, RF)

            # Display the predicted crop to the user
            st.success(f"The recommended crop is: {result}")
    with right_column:
        st.header("  ")
        st.header("  ")
        st.header("  ")
        st_lottie(lottie_coding,height=400,key="coding")

