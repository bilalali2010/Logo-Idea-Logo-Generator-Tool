import svgwrite
import random

def generate_logo_prompt(brand, desc=""):
    base = f"Create a modern, futuristic logo for '{brand}'. Use gradients, abstract shapes, clean geometry, and tech-inspired elements."
    if desc:
        base += f" Brand details: {desc}."
    return base + " Provide 5 creative variations."

def generate_logo_svg(brand, color):
    dwg = svgwrite.Drawing(size=("400px", "400px"))

    # Gradient definition
    gradient = dwg.linearGradient(start=("0%", "0%"), end=("100%", "100%"))
    gradient.add_stop_color("0%", color, opacity=0.95)
    gradient.add_stop_color("100%", "#000000", opacity=0.85)
    dwg.defs.add(gradient)

    # Background gradient circle
    dwg.add(
        dwg.circle(center=("200", "160"), r="110", fill=gradient.get_paint_server())
    )

    # Abstract tech line patterns
    for i in range(5):
        x1 = random.randint(80, 150)
        x2 = random.randint(250, 320)
        y = random.randint(90, 230)
        dwg.add(
            dwg.line(
                start=(x1, y),
                end=(x2, y),
                stroke="#ffffff",
                stroke_width=1,
                opacity=0.15,
            )
        )

    # Brand Initial
    dwg.add(
        dwg.text(
            brand[0].upper(),
            insert=("175", "190"),
            font_size="100px",
            fill="#ffffff",
            font_weight="bold",
        )
    )

    # Brand Name Below
    dwg.add(
        dwg.text(
            brand,
            insert=("140", "300"),
            font_size="28px",
            fill=color,
            style="font-family: sans-serif;",
        )
    )

    return dwg.tostring()
