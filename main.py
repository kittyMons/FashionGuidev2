
import streamlit as st
import requests
from openai import OpenAI

client = OpenAI(api_key = st.secrets['OPENAI_API_KEY'])

st.title("What's your outfit today?")

def ai_suggestion(images, occasion):
  response = OpenAI.ChatCompletion.create(
  model="gpt-4",
  messages = [
      {
        "role": 
        "user", 
        "content":[{
          "type":
          "text",
          "text":
          "I want suggestions for an outfit to go on a" + occasion},
                   {
                     "type": "image_url",
                     "image_url": 
                     {"url": images}
                   }
                  ]}
  ],
  max_tokens=200,
  )
  return response.choices[0].message["content"]


uploaded_files = st.file_uploader("Upload pictures of clothes or accessories", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    st.write("filename:", uploaded_file.name)
    st.write(bytes_data)


occasion = st.text_input("Enter the occasion for which you need an outfit suggestion (e.g., coffee date)")

if st.button("Get Suggestion"):
    if uploaded_files and occasion:
        image_urls = []
        suggestion = ai_suggestion(image_urls, occasion)


        st.write(suggestion)
    else:
      st.write(Please upload image)
