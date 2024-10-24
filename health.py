from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Configure the Generative AI model with the API key from environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro Vision API and get response
def get_gemini_response(input_prompt, image, user_input):
    model = genai.GenerativeModel('gemini-pro-vision')
    response = model.generate_content([input_prompt, image[0], user_input])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Initialize Streamlit app
st.set_page_config(page_title="NutriScan AI App", layout='wide')

st.title(" NutriScan AI App")
st.write("""
Welcome to the NutriScan AI App! This application uses advanced Generative AI to analyze food items from images
and calculate their total calories. Upload an image of food and provide a prompt to get detailed nutritional information.
""")

# Sidebar for input
st.sidebar.header("Upload and Input")
user_input = st.sidebar.text_input("Input Prompt: ", key="input", help="Enter your query about the food items")
uploaded_file = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    st.sidebar.image(uploaded_file, caption="Uploaded Image.", use_column_width=True)

submit = st.sidebar.button("Analyze Food")

input_prompt = """
You are an expert nutritionist. You need to analyze the food items from the image
and calculate the total calories. Also, provide the details of every food item with calorie intake
in the following format:

1. Item 1 - number of calories
2. Item 2 - number of calories
---
---
"""

# Main section to display results
if submit:
    with st.spinner("Analyzing the image..."):
        try:
            image_data = input_image_setup(uploaded_file)
            response = get_gemini_response(input_prompt, image_data, user_input)
            st.subheader("Calorie Analysis:")
            st.write(response)
        except FileNotFoundError as e:
            st.error(f"Error: {str(e)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")
else:
    st.info("Please upload an image and provide a prompt to analyze the food items.")
