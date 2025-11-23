## utils.py
```python
import svgwrite
import random
import math
import base64


# Supported shapes/styles
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


# Color palettes (simple lists of hex colors)
PALETTES = {
"Vibrant": ["#ff6b6b", "#f7b267", "#6bd4ff", "#8e6bff", "#3ddc97"],
"Modern Dark": ["#0f1724", "#1f2937", "#334155", "#64748b"],
"Pastel": ["#ffd6e0", "#bfe9ff", "#d7f7d9", "#fff3bf"],
"Mono": ["#111111", "#333333", "#666666"],
}


# helper: embed a local image file as data URI
def embed_image_as_datauri(path):
with open(path, "rb") as f:
raw = f.read()
return "data:image/png;base64," + base64.b64encode(raw).decode("utf-8")


# helper: short id-safe text
def sanify(text):
return "".join(c for c in text if c.isalnum() or c in (" ", "-", "_"))


# Core: generate a full SVG string for a given shape
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


bg = "#ffffff"
# white background rectangle so streamlit preview is stable
dwg.add(dwg.rect(insert=(0, 0), size=(size[0], size[1]), fill=bg))


group = dwg.g(id="logo_group")


# Decide colors
if bw:
main = "#111111"
accent = "#666666"
group.add(dwg.circle(center=(240, 160), r=60, fill="none", stroke=accent, stroke_width=18,
