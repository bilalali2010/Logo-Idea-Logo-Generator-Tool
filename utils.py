import svgwrite

def generate_logo_prompt(brand, desc=""):
    base = f"Create a modern, clean vector logo for '{brand}'. Style: minimal, geometric, flat design."
    if desc:
        base += f" Brand description: {desc}."
    return base + " Provide multiple unique variations."


def generate_logo_svg(brand, color):
    dwg = svgwrite.Drawing(size=(300, 300))

    # geometric shape
    dwg.add(dwg.circle(center=(150, 130), r=70, fill=color, opacity=0.8))

    # first letter
    dwg.add(dwg.text(brand[0].upper(), insert=(130, 165), font_size="80px", fill="#ffffff"))

    # brand name
    dwg.add(dwg.text(brand, insert=(70, 260), font_size="26px", fill=color))

    return dwg.tostring()
