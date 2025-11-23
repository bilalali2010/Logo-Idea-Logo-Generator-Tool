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
# Templates
# -------------------------
TEMPLATES = {
    "Modern Badge": {
        "shape": "Badge / Emblem",
        "palette": "Vibrant",
        "include_slogan": True,
        "custom_color": None
    },
    "Tech Node": {
        "shape": "Tech Symbol",
        "palette": "Modern Dark",
        "include_slogan": True,
        "custom_color": None
    },
    "Creative Splash": {
        "shape": "Paint Splash",
        "palette": "Pastel",
        "include_slogan": False,
        "custom_color": None
    },
    "Geometric Cube": {
        "shape": "Geometric Cube",
        "palette": "Mono",
        "include_slogan": True,
        "custom_color": None
    },
}

# -------------------------
# Helper functions
# -------------------------
def embed_image_as_datauri(path):
    with open(path, "rb") as f:
        raw = f.read()
    return "data:image/png;base64," + base64.b64encode(raw).decode("utf-8")

def sanify(text):
    return "".join(c for c in text if c.isalnum() or c in (" ", "-", "_")).replace(" ", "_")

# -------------------------
# Core logo generator
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
    dwg.add(dwg.rect(insert=(0,0), size=(size[0], size[1]), fill="#ffffff"))

    main_color = "#111111" if bw else color
    accent_color = "#666666" if bw else (palette[1] if palette and len(palette)>1 else "#888888")

    group = dwg.g(id="logo_group")

    # -------------------------
    # Shape drawing logic
    # -------------------------
    if shape == "Abstract Swirl":
        for i in range(6):
            cx = random.randint(80, 340)
            cy = random.randint(80, 340)
            r = random.randint(30, 80)
            opacity = random.uniform(0.3, 0.7)
            group.add(dwg.circle(center=(cx, cy), r=r, fill="none", stroke=random.choice(palette), stroke_width=8, opacity=opacity))

    elif shape == "Geometric Cube":
        for i in range(3):
            x = random.randint(50, 280)
            y = random.randint(50, 280)
            s = random.randint(60, 100)
            group.add(dwg.rect(insert=(x, y), size=(s, s), fill=random.choice(palette), stroke=accent_color, stroke_width=5, opacity=0.8))

    elif shape == "Rounded Blob":
        path_data = f"M{random.randint(100,150)},200 Q{random.randint(180,220)},100 {random.randint(250,300)},200 Q{random.randint(180,220)},300 {random.randint(100,150)},200 Z"
        group.add(dwg.path(d=path_data, fill=main_color, opacity=0.7))

    elif shape == "House / Roof":
        group.add(dwg.polygon(points=[(150,250),(210,150),(270,250)], fill=random.choice(palette)))  # roof
        group.add(dwg.rect(insert=(170,250), size=(80,80), fill=random.choice(palette)))             # house body
        group.add(dwg.rect(insert=(200,280), size=(20,50), fill=accent_color))                      # door

    elif shape == "Sports Ball":
        group.add(dwg.circle(center=(210,210), r=80, fill=random.choice(palette), stroke=accent_color, stroke_width=5))
        group.add(dwg.line(start=(210,130), end=(210,290), stroke=accent_color, stroke_width=3))
        group.add(dwg.line(start=(130,210), end=(290,210), stroke=accent_color, stroke_width=3))

    elif shape == "Tech Symbol":
        for i in range(5):
            x = random.randint(120,300)
            y = random.randint(120,300)
            group.add(dwg.circle(center=(x,y), r=10, fill=random.choice(palette)))
            group.add(dwg.line(start=(210,210), end=(x,y), stroke=accent_color, stroke_width=2))

    elif shape == "Badge / Emblem":
        group.add(dwg.circle(center=(210,210), r=100, fill=random.choice(palette), stroke=accent_color, stroke_width=5))
        group.add(dwg.circle(center=(210,210), r=70, fill="none", stroke=accent_color, stroke_width=3))

    elif shape == "Paint Splash":
        for i in range(8):
            cx = random.randint(100,320)
            cy = random.randint(100,320)
            r = random.randint(10,40)
            group.add(dwg.circle(center=(cx,cy), r=r, fill=random.choice(palette), opacity=random.uniform(0.3,0.7)))

    elif shape == "Linked Rings":
        for i in range(3):
            cx = 180 + i*50
            cy = 210
            group.add(dwg.circle(center=(cx,cy), r=40, fill="none", stroke=random.choice(palette), stroke_width=6, opacity=0.7))

    else:
        group.add(dwg.circle(center=(210,210), r=80, fill=main_color, stroke=accent_color, stroke_width=5))

    # -------------------------
    # Embed image if provided
    # -------------------------
    if embed_image_datauri:
        group.add(dwg.image(href=embed_image_datauri, insert=(150,150), size=(120,120)))

    dwg.add(group)

    # -------------------------
    # Add brand text inside shape
    # -------------------------
    text_font_size = 24 if len(brand) <= 12 else max(12, 24 - len(brand)//2)
    dwg.add(dwg.text(
        brand,
        insert=(size[0]//2, size[1]//2),
        text_anchor="middle",
        alignment_baseline="middle",
        font_size=text_font_size,
        fill=main_color,
        font_family="Arial",
        font_weight="bold"
    ))

    # Optional slogan inside shape, below brand
    if include_slogan and slogan:
        dwg.add(dwg.text(
            slogan,
            insert=(size[0]//2, size[1]//2 + text_font_size + 10),
            text_anchor="middle",
            alignment_baseline="hanging",
            font_size=16,
            fill=accent_color,
            font_family="Arial"
        ))

    return dwg.tostring()
