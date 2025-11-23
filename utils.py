import svgwrite
import random
import base64

# -------------------------
# Supported shapes/styles
# -------------------------
SHAPES = [
    "Abstract Swirl",
    "Geometric Cube",
    "Rounded Blob",
    "House / Roof",
    "Sports Ball",
    "Tech Symbol",
    "Badge / Emblem",
    "Paint Splash",
    "Linked Rings",
]

# -------------------------
# Color palettes
# -------------------------
PALETTES = {
    "Vibrant": ["#ff6b6b", "#f7b267", "#6bd4ff", "#8e6bff", "#3ddc97"],
    "Modern Dark": ["#0f1724", "#1f2937", "#334155", "#64748b"],
    "Pastel": ["#ffd6e0", "#bfe9ff", "#d7f7d9", "#fff3bf"],
    "Mono": ["#111111", "#333333", "#666666"],
}

# -------------------------
# Helper: embed local image as data URI
# -------------------------
def embed_image_as_datauri(path):
    with open(path, "rb") as f:
        raw = f.read()
    return "data:image/png;base64," + base64.b64encode(raw).decode("utf-8")

# -------------------------
# Helper: safe filename/text
# -------------------------
def sanify(text):
    return "".join(c for c in text if c.isalnum() or c in (" ", "-", "_")).replace(" ", "_")

# -------------------------
# Core: generate SVG logo
# -------------------------
def generate_logo_svg(
    brand,
    shape="Abstract Swirl",
    color="#1f77b4",
    include_slogan=False,
    slogan="",
    embed_image_datauri=None,
    bw=False,
    palette=None,
    seed=None,
):
    random.seed(seed)
    size = (420, 420)
    dwg = svgwrite.Drawing(size=(f"{size[0]}px", f"{size[1]}px"))

    # White background for preview stability
    dwg.add(dwg.rect(insert=(0, 0), size=(size[0], size[1]), fill="#ffffff"))

    group = dwg.g(id="logo_group")

    # Decide colors
    if bw:
        main_color = "#111111"
        accent_color = "#666666"
    else:
        main_color = color
        accent_color = palette[1] if palette and len(palette) > 1 else "#888888"

    # -------------------------
    # Draw simple shapes based on selection
    # -------------------------
    if shape == "Abstract Swirl":
        for i in range(5):
            cx = random.randint(80, 340)
            cy = random.randint(80, 340)
            r = random.randint(30, 80)
            group.add(dwg.circle(center=(cx, cy), r=r, fill="none", stroke=main_color, stroke_width=8, opacity=0.6))
    elif shape == "Geometric Cube":
        for i in range(3):
            x = random.randint(50, 300)
            y = random.randint(50, 300)
            size_cube = random.randint(60, 100)
            group.add(dwg.rect(insert=(x, y), size=(size_cube, size_cube), fill=main_color, stroke=accent_color, stroke_width=5, opacity=0.8))
    elif shape == "Rounded Blob":
        path = dwg.path(d=f"M150,200 Q200,100 250,200 Q200,300 150,200 Z", fill=main_color, opacity=0.7)
        group.add(path)
    else:
        # fallback: simple circle
        group.add(dwg.circle(center=(210, 210), r=80, fill=main_color, stroke=accent_color, stroke_width=6, opacity=0.8))

    # -------------------------
    # Embed image if provided
    # -------------------------
    if embed_image_datauri:
        group.add(dwg.image(href=embed_image_datauri, insert=(150, 150), size=(120, 120)))

    # -------------------------
    # Add brand text
    # -------------------------
    dwg.add(group)
    dwg.add(dwg.text(brand, insert=(size[0]//2, size[1]-50), text_anchor="middle", font_size=24, fill=main_color, font_family="Arial"))

    # Optional slogan
    if include_slogan and slogan:
        dwg.add(dwg.text(slogan, insert=(size[0]//2, size[1]-20), text_anchor="middle", font_size=16, fill=accent_color, font_family="Arial"))

    return dwg.tostring()
