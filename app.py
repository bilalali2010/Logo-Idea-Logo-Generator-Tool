import streamlit as st
from diffusers import StableDiffusionPipeline
import torch
from PIL import Image
import io

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="Logo Idea Generator", page_icon="🎨", layout="wide")

# -------------------------
# Sidebar
# -------------------------
st.sidebar.header("Settings")
hf_token = st.sidebar.text_input("Enter Hugging Face Token 🔑", type="password")

# -------------------------
# Main app
# -------------------------
st.title("🤖 Logo Idea & Generator Tool")
st.markdown("Generate creative logos using AI!")

prompt = st.text_input("Enter your logo idea prompt:")

# -------------------------
# Cache model loading
# -------------------------
@st.cache_resource(show_spinner=True)
def load_model(token):
    pipe = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5",
        use_auth_token=token
    )
    pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")
    return pipe

if st.button("Generate Logo"):

    if not hf_token:
        st.error("Please enter your Hugging Face token in the sidebar!")
    elif not prompt:
        st.error("Please enter a prompt for the logo!")
    else:
        try:
            with st.spinner("Loading model..."):
                pipe = load_model(hf_token)

            with st.spinner("Generating your logo..."):
                image = pipe(prompt).images[0]

                # Display image
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
