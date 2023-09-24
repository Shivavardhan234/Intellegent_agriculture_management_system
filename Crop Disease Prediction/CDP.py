import streamlit as st
import requests
from streamlit_lottie import st_lottie
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image


st.set_page_config(page_title="Crop Disease Prediction And Its Remedy Recommendation",layout="wide")

def load_lottieurl(url):
    r=requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()



def predict_class(image, model):
    
    # Preprocess the image.
    image = Image.open(image)
    image = image.resize((224, 224))
    image = np.array(image) / 255.0
    

    # Expand the image batch dimension.
    image = np.expand_dims(image, axis=0)

    # Make a prediction.
    prediction = model.predict(image)

    # Get the predicted class.
    predicted_class = np.argmax(prediction)

    # Return the predicted class.
    return predicted_class


def get_remedy(disease):
    remedies_dict = {
        'Cercospora Leaf Spot in maize': 'Apply pesticides like chlorothalonil or mancozeb, and practice crop rotation.',
        'Common Rust in maize': 'Use pesticides like triazoles or strobilurins, and plant resistant maize varieties.',
        'Northern Leaf Blight in maize': 'Apply pesticides like azoxystrobin or pyraclostrobin, and use resistant maize varieties.',
        'Early blight in potato': 'Use pesticides like chlorothalonil or copper-based sprays, and practice crop rotation.',
        'Late Blight in potato': 'Apply pesticides like mancozeb or metalaxyl, and practice crop rotation.',
        'Bacterial spot in tomato': 'Use copper-based sprays, practice good sanitation, and avoid overhead irrigation.',
        'Early blight in tomato': 'Apply pesticides like chlorothalonil or copper-based sprays, and prune infected leaves.',
        'Late Blight in tomato': 'Use pesticides like mancozeb or metalaxyl, and practice proper plant spacing and ventilation.',
        'Septoria leaf spot in tomato': 'Apply pesticides like chlorothalonil or azoxystrobin, and remove infected leaves.',
        'Yellow leaf curl virus in tomato': 'Plant virus-resistant tomato varieties and control whitefly vectors with insecticides.'
    }
    return remedies_dict.get(disease, 'Maintain good agricultural practices and monitor for early signs of diseases.')


st.title("Crop Disease Prediction And Remedy Recommendation 🌾")


lottie_coding=load_lottieurl("https://lottie.host/8e0b2d84-9b97-4872-ab84-e50eef454d51/dn8exImHZP.json")


with st.container():
    st.write("---")
    left_column,right_column=st.columns(2)
    with left_column:
        st.header("About this website")
        st.write("""Crop Disease Prediction and Remedy Recommendation is a Deep learning project .It takes crop name and image of the leaf as inputs and predicts its disease.It also recommends remedy to that particular disease. """)
        st.write("""Currently it only sonsists of only data of three crops (maize ,potato and tomato)""")
        st.header("  ")
        X=st.text_input("Enter the name of the crop")


        upload=st.file_uploader("chose a crop diseased leaf image file",type='jpg')

        if st.button("Predict"):

            if ((X is not None) and(upload is not None)):
                # Add a button to call the prediction function
            
                if (X=='maize'):
                    # Load the model.
                    model = load_model("model1.h5")


                    # Predict the class of the image.
                    predicted_class = int(predict_class(upload, model))
                    disease=['Cercospora Leaf Spot in maize','Common Rust in maize','Healthy maize crop','Northern Leaf Blight in maize']
                    

                    predicted_disease=disease[predicted_class]
                    st.header("Crop Disease")
                    # Display the predicted crop to the user
                    st.success(f"The predicted crop disease is: {predicted_disease}")
                    st.header("Remedies")
                    result=get_remedy(predicted_disease)
                    st.success(f" {result}")

                elif(X=='potato'):
                    # Load the model.
                    model = load_model("potatoo.h5")


                    # Predict the class of the image.
                    predicted_class = int(predict_class(upload, model))
                    disease=['Early blight in potato','Healthy potato crop','Late Blight in potato']
                    
                    predicted_disease=disease[predicted_class]
                    st.header("Crop Disease")
                    # Display the predicted crop to the user
                    st.success(f"The predicted crop disease is: {predicted_disease}")
                    st.header("Remedies")
                    result=get_remedy(predicted_disease)
                    st.success(f" {result}")

                   
                elif(X=='tomato'):
                        # Load the model.
                    model = load_model("tomatoo.h5")


                    # Predict the class of the image.
                    predicted_class = predict_class(upload, model)
                    disease=['Bacterial spot in tomato','Early blight in tomato','Healthy tomato crop','Late Blight in tomato','Septoria leaf spot in tomato','Yellow leaf curl virus in tomato']

                    predicted_disease=disease[predicted_class]
                    st.header("Crop Disease")
                    # Display the predicted crop to the user
                    st.success(f"The predicted crop disease is: {predicted_disease}")
                    st.header("Remedies")
                    result=get_remedy(predicted_disease)
                    st.success(f" {result}")

                

            else:
                
                st.header("Error")
                # Display the predicted crop to the user
                st.error(f"Enter the crop name and upload the image")
    with right_column:
        st.header("  ")
        st.header("  ")
        st.header("  ")
        st_lottie(lottie_coding,height=400,key="coding")