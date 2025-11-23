import streamlit as st
from utils import generate_logo_svg, generate_logo_prompt

st.set_page_config(page_title="AI Logo Generator", layout="wide")

st.title("🎨 AI Logo & Logo Idea Generator")
st.write("Generate unique logo prompts or instantly create minimal SVG logos — 100% free & CPU-friendly.")

mode = st.radio("Choose Mode", ["Generate Logo Idea Prompt", "Generate Simple SVG Logo"])

# -------------------------
# LOGO PROMPT GENERATOR
# -------------------------
if mode == "Generate Logo Idea Prompt":
    brand = st.text_input("Brand Name")
    desc = st.text_area("Describe your brand (optional)")

    if st.button("Generate Prompt"):
        if brand.strip() == "":
            st.error("Brand name required.")
        else:
            prompt = generate_logo_prompt(brand, desc)
            st.success("Prompt generated:")
            st.code(prompt)

# -------------------------
# SVG LOGO GENERATOR
# -------------------------
else:
    brand = st.text_input("Brand Name for SVG Logo")
    color = st.color_picker("Choose Logo Color", "#000000")

    if st.button("Generate SVG Logo"):
        if brand.strip() == "":
            st.error("Brand name required.")
        else:
            svg = generate_logo_svg(brand, color)
            st.success("SVG Logo Generated:")
            st.code(svg, language="xml")
            st.download_button("Download SVG Logo", svg, f"{brand}_logo.svg")
