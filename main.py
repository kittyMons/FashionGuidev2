import streamlit as st
import requests
import openai
from PIL import Image
import io

client = OpenAI(api_key= st.secrets['OPENAI_API_KEY'],)

st.title("What's your outfit today?")

def ai_suggestion(items, occasion):
    prompt = f"Based on the following items: {', '.join(items)} and the occasion: {occasion}, suggest an outfit."
    
    fashion_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a fashion assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=200,
    )
    response = fashion_response.choices[0].message.content
    return response


uploaded_files = st.file_uploader("Upload pictures of clothes or accessories", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
items = []
for uploaded_file in uploaded_files:
    image = Image.open(io.BytesIO(uploaded_file.read()))

occasion = st.text_input("Enter the occasion for which you need an outfit suggestion (e.g., coffee date)")

if st.button("Get Suggestion"):
    if items and occasion:
        suggestion = ai_suggestion(items, occasion)
        st.write(suggestion)
    else:
        st.write("Please upload images and enter an occasion")
