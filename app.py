# app.py
import streamlit as st
from utils import generate_logo_svg, generate_logo_prompt


st.set_page_config(page_title="AI Logo Generator", layout="wide")


st.title("🎨 AI Logo & Logo Idea Generator")
st.write("Generate unique logo prompts or instantly create minimal SVG logos — 100% free & CPU‑friendly.")


mode = st.radio("Choose Mode", ["Generate Logo Idea Prompt", "Generate Simple SVG Logo"])


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




# utils.py
import svgwrite


# Generate AI-styled logo prompt
def generate_logo_prompt(brand, desc=""):
base = f"Create a modern, clean vector logo for the brand '{brand}'. Style: minimal, geometric, flat design."
if desc:
base += f" Brand description: {desc}."
return base + " Provide multiple unique variations."




# Minimal SVG Logo generator (CPU‑friendly)
def generate_logo_svg(brand, color):
dwg = svgwrite.Drawing(size=(300, 300))


# geometric circle background
dwg.add(dwg.circle(center=(150, 130), r=70, fill=color, opacity=0.8))


# first letter icon
dwg.add(dwg.text(brand[0].upper(), insert=(130, 165), font_size="80px", fill="#ffffff"))


# brand name
dwg.add(dwg.text(brand, insert=(70, 260), font_size="26px", fill=color))


return dwg.tostring()
