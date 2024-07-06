import streamlit as st
import openai
import base64
import requests

client = openai.OpenAI(api_key=st.secrets['OPENAI_API_KEY'])

st.title("What's your outfit today?")

def ai_suggestion(occasion, uploaded_images):
    prompt = f"You are a fashion assistant. Although I can't see any uploaded outfits, I can certainly help you suggest an outfit for a {occasion} based on an inventory list. Let’s imagine a basic wardrobe and I’ll put together an outfit for you."
    
    # Append comments about each uploaded image
    if uploaded_images:
        prompt += "\n\n**Uploaded Outfits:**"
        for idx, image in enumerate(uploaded_images):
            prompt += f"\n\n**Uploaded Image {idx+1}:**"
            prompt += f"\n![Uploaded Image {idx+1}]({image})"
            prompt += f"\nComment: Describe the outfit in the image and whether it's suitable for the occasion."
    
    fashion_response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a fashion assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=400,  # Adjust max_tokens as needed
    )
    response = fashion_response.choices[0].message.content
    return response

def encode_image(uploaded_file):
    # Read the bytes data from BytesIO object
    bytes_data = uploaded_file.read()
    # Encode bytes data to base64
    encoded_image = base64.b64encode(bytes_data).decode('utf-8')
    return f"data:image/png;base64,{encoded_image}"

uploaded_files = st.file_uploader("Upload pictures of clothes or accessories", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

# Display uploaded images in a horizontal row
uploaded_images = []
if uploaded_files:
    columns = st.columns(len(uploaded_files))
    for column, uploaded_file in zip(columns, uploaded_files):
        column.image(uploaded_file, use_column_width=True)
        # Encode and store uploaded image
        uploaded_images.append(encode_image(uploaded_file))

occasion = st.text_input("Enter the occasion for which you need an outfit suggestion (e.g., restaurant date)")

if st.button("Get Suggestion"):
    if occasion:
        suggestion = ai_suggestion(occasion, uploaded_images)
        st.markdown(suggestion)  # Display suggestion formatted with markdown
    else:
        st.write("Please enter an occasion.")
