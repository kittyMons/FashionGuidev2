import streamlit as st
import openai
import base64
import requests

client = openai.OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

st.title("What's your outfit today?")

def ai_suggestion(items, occasion):
    prompt = f"You are a fashion assistant. Based on the following items and the occasion ({occasion}), suggest an outfit and provide feedback on the uploaded outfits:"
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

def encode_image(file_path):
    with open(file_path, 'rb') as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def vision_file(file_path):
    base64_image = encode_image(file_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {st.secrets['OPENAI_API_KEY']}"
    }

    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "user", "content": [
                {"type": "text", "text": "what is in this image?"},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
            ]}
        ],
        "max_tokens": 20
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    st.write(response.json()['choices'][0]['message']['content'])

uploaded_files = st.file_uploader("Upload pictures of clothes or accessories", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Display uploaded images in a horizontal row
if uploaded_files:
    columns = st.columns(len(uploaded_files))
    for column, uploaded_file in zip(columns, uploaded_files):
        bytes_data = uploaded_file.read()
        column.image(bytes_data, use_column_width=True)

occasion = st.text_input("Enter the occasion for which you need an outfit suggestion (e.g., coffee date)")

if st.button("Get Suggestion"):
    if uploaded_files and occasion:
        image_urls = []
        suggestion = ai_suggestion(image_urls, occasion)
        st.write(suggestion)
    else:
        st.write("Please upload images and enter an occasion.")
