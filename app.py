import streamlit as st
from PIL import Image
import requests
import io

# -------------------------
# Page Config
# -------------------------
st.set_page_config(page_title="Free Logo Generator", page_icon="🎨", layout="wide")

st.title("🎨 Free Logo Idea & Generator Tool")
st.markdown("Generate **creative logo ideas** and **AI-generated logos** for your brand using free tools!")

# -------------------------
# User Inputs
# -------------------------
brand_name = st.text_input("Brand Name")
industry = st.text_input("Industry")
style = st.selectbox("Logo Style", ["Minimal", "Modern", "Playful", "Elegant"])

# -------------------------
# Generate Logo Idea (Text Only)
# -------------------------
if st.button("Generate Logo Idea"):
    if brand_name and industry:
        idea = f"💡 Logo idea: '{brand_name}' for the {industry} industry in {style} style. Consider using bold initials, icon representing {industry}, and colors that fit the {style} theme."
        st.success(idea)
    else:
        st.warning("Please enter both Brand Name and Industry.")

# -------------------------
# Generate Logo Image (Free)
# -------------------------
st.markdown("---")
st.subheader("Generate Logo Image (Free)")

# Select free model
generator_option = st.selectbox(
    "Choose Free Logo Generator",
    ["Craiyon (Free, Quick)", "Replicate Stable Diffusion (Free Tier, Needs API Key)"]
)

# Craiyon Generation
if generator_option == "Craiyon (Free, Quick)":
    if st.button("Generate Logo Image with Craiyon"):
        if brand_name:
            st.info("Generating logo using Craiyon... This may take 20-40 seconds.")
            # Craiyon API call
            craiyon_url = f"https://craiyon.com/api?prompt={brand_name}+logo+{style}+{industry}"
            try:
                response = requests.get(craiyon_url)
                if response.status_code == 200:
                    st.image(response.content, caption="Generated Logo", use_column_width=True)
                else:
                    st.error("Failed to generate image from Craiyon.")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter Brand Name.")

# Replicate Stable Diffusion (Optional)
if generator_option == "Replicate Stable Diffusion (Free Tier, Needs API Key)":
    replicate_api_key = st.text_input("Enter your Replicate API Key (Free Tier)", type="password")
    if st.button("Generate Logo Image with Stable Diffusion"):
        if replicate_api_key and brand_name:
            st.info("Generating logo with Stable Diffusion... This may take 30-60 seconds.")
            import replicate

            try:
                client = replicate.Client(api_token=replicate_api_key)
                model = client.models.get("stability-ai/stable-diffusion")
                prompt = f"{brand_name} logo, {style} style, {industry}, minimal, vector"
                output_url = model.predict(prompt=prompt, width=512, height=512)[0]
                st.image(output_url, caption="Generated Logo", use_column_width=True)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter Brand Name and API Key.")

# -------------------------
st.markdown("---")
st.caption("Built with ❤️ using Streamlit | Completely Free")
