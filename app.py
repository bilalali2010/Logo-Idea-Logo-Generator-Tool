import streamlit as st
import requests
from PIL import Image
import io
import base64

st.set_page_config(page_title="Logo Idea Generator", page_icon="🎨", layout="wide")

st.sidebar.header("Settings")
hf_token = st.sidebar.text_input("Enter Hugging Face Token 🔑", type="password")

st.title("🤖 Logo Idea & Generator Tool")
prompt = st.text_input("Enter your logo idea prompt:")

if st.button("Generate Logo"):

    if not hf_token:
        st.error("Please enter your Hugging Face token in the sidebar!")
    elif not prompt:
        st.error("Please enter a prompt for the logo!")
    else:
        try:
            st.info("Generating your logo...")

            headers = {"Authorization": f"Bearer {hf_token}"}
            API_URL = "https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5"

            payload = {"inputs": prompt}

            response = requests.post(API_URL, headers=headers, json=payload)
            
            if response.status_code != 200:
                st.error(f"Error: {response.status_code}, {response.text}")
            else:
                image_bytes = response.content
                image = Image.open(io.BytesIO(image_bytes))
                st.image(image, caption="Generated Logo", use_column_width=True)

                # Download option
                buf = io.BytesIO()
                image.save(buf, format="PNG")
                st.download_button(
                    label="Download Logo",
                    data=buf,
                    file_name="generated_logo.png",
                    mime="image/png"
                )

        except Exception as e:
            st.error(f"Failed to generate image: {e}")
