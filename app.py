# AI Logo Generator — Multi-Shape (Streamlit)


This file set contains a ready-to-deploy Streamlit app that generates professional SVG logos in multiple styles (abstract swirl, geometric cube, rounded blob, house/roof, sports ball, tech symbol, badge/emblem, paint splash, linked rings). It includes color palettes, optional slogan generation, and the ability to embed a raster image (sample file included).


---


## app.py
```python
import streamlit as st
from utils import (
generate_logo_svg,
PALETTES,
SHAPES,
embed_image_as_datauri,
)
import base64


st.set_page_config(page_title="AI Logo Generator — Multi Shape", layout="wide")
st.title("AI Logo Generator — Multi-Shape Professional Logos")
st.write("Generate modern, high-quality SVG logos in multiple styles. No GPU required — pure SVG + Python.")


# ----- Sidebar -----
with st.sidebar:
st.header("Generator Settings")
brand = st.text_input("Brand name", value="Bilal Tech")
slogan = st.text_input("Slogan (optional)")


st.markdown("**Styles**")
selected = st.multiselect("Choose shapes/styles (you can pick multiple)", SHAPES, default=[SHAPES[0]])


st.markdown("**Colors**")
palette_choice = st.selectbox("Palette", list(PALETTES.keys()))
color_mode = st.radio("Color mode", ["Palette (recommended)", "Custom main color", "Black & White"], index=0)
custom_color = None
if color_mode == "Custom main color":
custom_color = st.color_picker("Choose main color", "#1f77b4")


st.markdown("**Output**")
n_variations = st.slider("How many variations to generate", 1, 6, 3)
include_slogan = st.checkbox("Include slogan under the logo", value=bool(slogan))
embed_sample = st.checkbox("Embed sample image inside logo (demo)")


st.markdown("**Input image**")
uploaded_file = st.file_uploader("Upload an icon or image to embed (optional)")
# developer-provided sample file path (local). We'll use this as a demo default when user checks the sample box.
sample_local_path = "/mnt/data/A_2D_digital_graphic_design_compilation_features_n.png"


# ----- Generate -----
cols = st.columns(2)
with cols[0]:
st.subheader("Preview")
with cols[1]:
st.subheader("SVG Code / Download")


if st.button("Generate Logos"):
palettes = PALETTES[palette_choice]


# decide image data uri if embedding
image_datauri = None
if uploaded_file is not None:
# convert uploaded bytes to datauri
raw = uploaded_file.read()
image_datauri = "data:image/png;base64," + base64.b64encode(raw).decode("utf-8")
elif embed_sample:
try:
image_datauri = embed_image_as_datauri(sample_local_path)
except Exception as e:
st.warning(f"Could not embed sample image: {e}")
image_datauri = None


generated_svgs = []
for i in range(n_variations):
shape = selected[i % len(selected)]
main_color = custom_color if custom_color else palettes[i % len(palettes)]
bw = color_mode == "Black & White"


svg = generate_logo_svg(
brand=brand,
shape=shape,
color=main_color,
include_slogan=include_slogan,
slogan=slogan,
embed_image_datauri=image_datauri,
bw=bw,
palette=palettes,
seed=i,
)
generated_svgs.append((shape, svg))


# Display results in a grid
cols = st.columns(3)
for idx, (shape, svg) in enumerate(generated_svgs):
