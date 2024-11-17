import streamlit as st
import requests
import firebase_admin
from firebase_admin import credentials, db
from streamlit_lottie import st_lottie
import time

# Function to load Lottie animation
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Firebase setup (initialize once)
if not firebase_admin._apps:
    cred = credentials.Certificate('crop-management-b68d3-6108a91f5804.json')  # Replace with the path to your Firebase credentials file
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://crop-management-b68d3-default-rtdb.firebaseio.com/'  # Replace with your Firebase Realtime Database URL
    })

# Set up the page configuration
st.set_page_config(page_title="Crop Management System", layout="wide")

# Title of the page
st.title("Crop Management System 🌱")

# Lottie animation
lottie_coding = load_lottieurl("https://lottie.host/8e0b2d84-9b97-4872-ab84-e50eef454d51/dn8exImHZP.json")

# Initialize session state if not already initialized
if 'auto_control' not in st.session_state:
    st.session_state.auto_control = False
if 'pump_ctrl' not in st.session_state:
    st.session_state.pump_ctrl = False  # For pump control state

# Function to update Firebase with current state
def update_firebase():
    # Reference to the Firebase database
    ref = db.reference('crop_management')  # Change this path as needed in the database
    ref.set({
        'auto_control': st.session_state.auto_control,
    })
    
    # Update IAMS/auto_pump based on auto_control state
    ref_auto_pump = db.reference('IAMS/auto_pump')
    if st.session_state.auto_control:
        ref_auto_pump.set(1)  # Set auto_pump to 1 when auto_control is on
    else:
        ref_auto_pump.set(0)  # Set auto_pump to 0 when auto_control is off
    
    # Update pump control status in IAMS
    ref_pump_ctrl = db.reference('IAMS/pump_ctrl')
    if st.session_state.pump_ctrl:
        ref_pump_ctrl.set(1)  # Set pump_ctrl to 1 when pump is activated
    else:
        ref_pump_ctrl.set(0)  # Set pump_ctrl to 0 when pump is deactivated

# Fetch real-time data from Firebase
def fetch_sensor_data():
    try:
        ref_temp = db.reference('IAMS/temp')
        ref_hum = db.reference('IAMS/hum')
        ref_moist = db.reference('IAMS/moist')
        ref_waterlevel = db.reference('IAMS/waterlevel')
        
        temperature = ref_temp.get()
        humidity = ref_hum.get()
        moisture = ref_moist.get()
        water_level = ref_waterlevel.get()
        
        return temperature, humidity, moisture, water_level
    except Exception as e:
        st.error(f"Error fetching data from Firebase: {e}")
        return None, None, None, None

# Fetch pump status from Firebase
def fetch_pump_status():
    try:
        ref_pump_status = db.reference('IAMS/pumpstatus')
        pump_status = ref_pump_status.get()
        return pump_status
    except Exception as e:
        st.error(f"Error fetching pump status from Firebase: {e}")
        return None

# Fetch auto control status from Firebase
def fetch_auto_control_status():
    try:
        ref_auto_pump = db.reference('IAMS/auto_pump')
        auto_control_status = ref_auto_pump.get()
        return auto_control_status
    except Exception as e:
        st.error(f"Error fetching auto control status from Firebase: {e}")
        return None

# Displaying content in a container
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    
    with left_column:
        st.header("Real-time Crop Monitoring")
        st.write(""" 
        This section displays real-time data for monitoring environmental factors in agricultural land:
        - Temperature
        - Humidity
        - Moisture
        - Water level
        """)

        # Create placeholders for data
        temp_placeholder = st.empty()
        humidity_placeholder = st.empty()
        moisture_placeholder = st.empty()
        water_level_placeholder = st.empty()
        auto_control_placeholder = st.empty()
        pump_placeholder = st.empty()

        # Add buttons for controlling auto-control
        if st.button('Toggle Auto-Control'):
            st.session_state.auto_control = not st.session_state.auto_control
            if st.session_state.auto_control:
                st.success("Auto-Control Enabled")
            else:
                st.success("Auto-Control Disabled")
            
            # Update Firebase when auto_control is toggled
            update_firebase()

        # Add button to toggle pump control
        if st.button('Toggle Pump'):
            st.session_state.pump_ctrl = not st.session_state.pump_ctrl
            if st.session_state.pump_ctrl:
                st.success("Pump Activated")
            else:
                st.success("Pump Deactivated")
            
            # Update Firebase when pump_ctrl is toggled
            update_firebase()

        while True:
            # Fetch real-time data from Firebase
            temperature, humidity, moisture, water_level = fetch_sensor_data()
            if temperature is not None and humidity is not None and moisture is not None and water_level is not None:
                # Update the placeholders with the latest data
                temp_placeholder.write(f"**Temperature**: {temperature} °C")
                humidity_placeholder.write(f"**Humidity**: {humidity} %")
                moisture_placeholder.write(f"**Soil Moisture**: {moisture} %")
                water_level_placeholder.write(f"**Water Level**: {water_level} cm")

            # Fetch pump status from Firebase
            pump_status = fetch_pump_status()
            if pump_status is not None:
                if pump_status:
                    pump_status_display = "On"
                else:
                    pump_status_display = "Off"
            else:
                pump_status_display = "Unknown"

            # Fetch auto-control status from Firebase
            auto_control_status = fetch_auto_control_status()
            if auto_control_status == 1:
                st.session_state.auto_control = True
            elif auto_control_status == 0:
                st.session_state.auto_control = False

            # Fetch auto-control status from session
            auto_control_display = "On" if st.session_state.auto_control else "Off"

            # Update the status placeholders
            auto_control_placeholder.write(f"**Auto-Control**: {auto_control_display}")
            pump_placeholder.write(f"**Pump**: {pump_status_display}")

            time.sleep(5)  # Wait for 5 seconds before fetching the data again

    with right_column:
        st.header("  ")
        st.header("  ")
        st.header("  ")
        st_lottie(lottie_coding, height=400, key="coding")
