import streamlit as st
from utils import (
    generate_logo_svg,
    PALETTES,
    SHAPES,
    embed_image_as_datauri,
    sanify
)
import base64

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="AI Logo Generator — Multi Shape", layout="wide")
st.title("AI Logo Generator — Multi-Shape Professional Logos")
st.write("Generate modern, high-quality SVG logos in multiple styles. No GPU required — pure SVG + Python.")

# -------------------------
# Sidebar settings
# -------------------------
with st.sidebar:
    st.header("Generator Settings")
    brand = st.text_input("Brand name", value="Bilal Tech")
    slogan = st.text_input("Slogan (optional)")
    color_palette = st.selectbox("Color Palette", list(PALETTES.keys()))
    shape_style = st.selectbox("Shape Style", SHAPES)
    n_variations = st.slider("How many variations to generate", 1, 6, 3)
    include_slogan = st.checkbox("Include slogan under the logo", value=bool(slogan))
    embed_sample = st.checkbox("Embed sample image inside logo (demo)")

# Multiple shape selection
st.markdown("**Styles**")
selected_shapes = st.multiselect(
    "Choose shapes/styles (you can pick multiple)",
    SHAPES,
    default=[SHAPES[0]]
)

# Color options
st.markdown("**Colors**")
palette_choice = st.selectbox("Palette", list(PALETTES.keys()))
color_mode = st.radio("Color mode", ["Palette (recommended)", "Custom main color", "Black & White"], index=0)
custom_color = None
if color_mode == "Custom main color":
    custom_color = st.color_picker("Choose main color", "#1f77b4")

# Image upload
st.markdown("**Input image**")
uploaded_file = st.file_uploader("Upload an icon or image to embed (optional)")
sample_local_path = "/mnt/data/A_2D_digital_graphic_design_compilation_features_n.png"

# -------------------------
# Logo generation
# -------------------------
if st.button("Generate Logos"):
    palettes = PALETTES[palette_choice]

    # Decide image data URI if embedding
    image_datauri = None
    if uploaded_file is not None:
        raw = uploaded_file.read()
        image_datauri = "data:image/png;base64," + base64.b64encode(raw).decode("utf-8")
    elif embed_sample:
        try:
            image_datauri = embed_image_as_datauri(sample_local_path)
        except Exception as e:
            st.warning(f"Could not embed sample image: {e}")
            image_datauri = None

    # Generate SVGs
    generated_svgs = []
    for i in range(n_variations):
        shape = selected_shapes[i % len(selected_shapes)]
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
    st.markdown("### Generated Logos")
    cols = st.columns(3)
    for idx, (shape, svg) in enumerate(generated_svgs):
        with cols[idx % 3]:
            st.write(f"**{shape}**")
            st.components.v1.html(svg, height=450)
            st.download_button(
                label="Download SVG",
                data=svg,
                file_name=f"{sanify(brand)}_{idx+1}.svg",
                mime="image/svg+xml"
            )
