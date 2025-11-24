import streamlit as st
from utils import (
    generate_logo_svg,
    PALETTES,
    SHAPES,
    embed_image_as_datauri,
    sanify,
    TEMPLATES
)
import base64

# -------------------------
# Page config
# -------------------------
st.set_page_config(page_title="AI Logo Generator — Multi Shape", layout="wide")
st.title("AI Logo Generator — Multi-Shape Professional Logos")
st.write("Generate modern, high-quality SVG logos in multiple styles. No GPU required — pure SVG + Python.")

# ⭐ ADDED MESSAGE ⭐
st.markdown("""
### ℹ️ Tip: in Mobile phone Click the *double arrow ( > ) on the top-left sidebar* to edit your Brand Name, Slogan, Colors and Styles.
""")

# -------------------------
# Template selection
# -------------------------
st.markdown("*Templates*")
selected_template_name = st.selectbox("Choose a starting template (optional)", ["None"] + list(TEMPLATES.keys()))

# Default settings
shape_style = SHAPES[0]
palette_choice = list(PALETTES.keys())[0]
include_slogan = False
custom_color = None

if selected_template_name != "None":
    template = TEMPLATES[selected_template_name]
    shape_style = template["shape"]
    palette_choice = template["palette"]
    include_slogan = template.get("include_slogan", False)
    custom_color = template.get("custom_color", None)
    
    # Show template preview
    svg_preview = generate_logo_svg(
        brand="Sample",
        shape=template["shape"],
        color=template["custom_color"] or PALETTES[template["palette"]][0],
        include_slogan=template.get("include_slogan", False),
        slogan="Your Slogan",
        palette=PALETTES[template["palette"]],
        seed=0
    )
    st.markdown("*Template Preview:*")
    st.components.v1.html(svg_preview, height=200)

# -------------------------
# Sidebar settings
# -------------------------
with st.sidebar:
    st.header("Generator Settings")
    brand = st.text_input("Brand name", value="write your brand name")
    slogan = st.text_input("Slogan (optional)")
    color_palette = st.selectbox("Color Palette", list(PALETTES.keys()), index=list(PALETTES.keys()).index(palette_choice))
    shape_style = st.selectbox("Shape Style", SHAPES, index=SHAPES.index(shape_style))
    n_variations = st.slider("How many variations to generate", 1, 6, 3)
    include_slogan = st.checkbox("Include slogan under the logo", value=include_slogan)
    embed_sample = st.checkbox("Embed sample image inside logo (demo)")

# Multiple shape selection
st.markdown("*Styles*")
selected_shapes = st.multiselect(
    "Choose shapes/styles (you can pick multiple)",
    SHAPES,
    default=[shape_style]
)

# Color options
st.markdown("*Colors*")
palette_choice = st.selectbox("Palette", list(PALETTES.keys()), index=list(PALETTES.keys()).index(palette_choice))
color_mode = st.radio("Color mode", ["Palette (recommended)", "Custom main color", "Black & White"], index=0)
if color_mode == "Custom main color" and custom_color is None:
    custom_color = st.color_picker("Choose main color", "#1f77b4")

# Image upload
st.markdown("*Input image*")
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
            st.write(f"*{shape}*")
            st.components.v1.html(svg, height=450)
            st.download_button(
                label="Download SVG",
                data=svg,
                file_name=f"{sanify(brand)}_{idx+1}.svg",
                mime="image/svg+xml"
            )
