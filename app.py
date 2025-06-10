import streamlit as st
import numpy as np
import cv2
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.efficientnet import preprocess_input
from PIL import Image


# Load trained model
@st.cache_resource
def load_trained_model():
    return load_model("deepfake_detector.h5")


model = load_trained_model()


# Function to preprocess image
def preprocess_image(image):
    image = image.resize((224, 224))
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image = preprocess_input(image)
    image = np.expand_dims(image, axis=0)
    return image


# Streamlit UI
st.title("🕵️ AI-Powered Deepfake Detector")
st.write("Upload an image to check if it's real or fake.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Clear previous results when a new image is uploaded
if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Show processing message
    with st.spinner("Processing Image..."):
        processed_image = preprocess_image(image)
        prediction = model.predict(processed_image)
        confidence = prediction[0][0] * 100  # Convert to percentage

    # Display results after processing
    if confidence < 1:
        st.error(f"🔴 Fake Image Detected!")
    else:
        st.success(f"✅ Real Image Detected!")

st.write("Trained on a custom deepfake dataset.")
