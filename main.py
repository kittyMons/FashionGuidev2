import streamlit as st
import openai
import base64
import requests

client = openai.OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

st.title("What's your outfit today?")

def ai_suggestion(items, occasion):
    prompt = f"You are a fashion assistant. Based on the following items and the occasion ({occasion}), suggest an outfit and provide feedback on the uploaded outfits:"

    # Call Gemini API for outfit suggestion
    gemini_response = genai.image2text(
        input=f"Based on the following items: {', '.join(items)} and the occasion: {occasion}, suggest an outfit.",
        model="gemini",
        max_length=200
    )

    response = gemini_response['text']
    return response

def encode_image(file):
    bytes_data = file.read()
    return base64.b64encode(bytes_data).decode('utf-8')

uploaded_files = st.file_uploader("Upload pictures of clothes or accessories", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Display uploaded images in a horizontal row
uploaded_images = []
if uploaded_files:
    columns = st.columns(len(uploaded_files))
    for column, uploaded_file in zip(columns, uploaded_files):
        bytes_data = uploaded_file.read()
        column.image(bytes_data, use_column_width=True)
        uploaded_images.append(f"data:image/png;base64,{encode_image(uploaded_file)}")

occasion = st.text_input("Enter the occasion for which you need an outfit suggestion (e.g., coffee date)")

if st.button("Get Suggestion"):
    if uploaded_images and occasion:
        suggestion = ai_suggestion(uploaded_images, occasion)
        st.write(suggestion)
    else:
        st.write("Please upload images and enter an occasion.")
