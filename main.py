import streamlit as st
import requests
from openai import OpenAI


client = OpenAI(api_key = st.secrets['OPENAI_API_KEY'])

def ai_suggestion(thumbnail,price):
  response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
              {
                "role":"user",
                "content":[{
                "type":"text", "text":"What is in this image?",
                "text":"is this product worth RM" + str(price) + "xxx price?"
                },
                {
                    "type":"image_url",
                    "image_url":{
                        "url":thumbnail
                    }
                }
            ]
        }
    ],
    max_tokens=50,
  )

  return response.choices[0].message.content

st.title('Cart')

uploaded_files = st.file_uploader("Upload pictures of clothes or accessories", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

response = requests.get('https://dummyjson.com/carts')
product_name=response.json()['carts'][0]['products'][0]['title']
product_price = response.json()['carts'][0]['products'][1]['price']
product_thumbnail = response.json()['carts'][0]['products'][1]['thumbnail']
import streamlit as st
import requests
from openai import OpenAI

client = OpenAI(api_key = st.secrets['OPENAI_API_KEY'])

st.title("What's your outfit today?")

def ai_suggestion(images, occasion):
  response = openai.ChatCompletion.create(
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