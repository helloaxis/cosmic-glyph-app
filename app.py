import os
import math
import io
from flask import Flask, request, send_file
import cairosvg

app = Flask(__name__)

def digit_sum(n):
    return sum(int(d) for d in str(n) if d.isdigit())

def extract_structure(date):
    year, month, day = date.split("-")

    total_sum = digit_sum(date.replace("-", ""))
    year_sum = digit_sum(year)
    month_sum = digit_sum(month)
    day_sum = digit_sum(day)

    polarity = total_sum % 2
    cycle = total_sum % 12 + 1

    return {
        "total": total_sum,
        "year": year_sum,
        "month": month_sum,
        "day": day_sum,
        "polarity": polarity,
        "cycle": cycle
    }

def generate_svg(date1, date2):
    s1 = extract_structure(date1)
    s2 = extract_structure(date2)

    center_x = 200
    center_y = 200
    radius = 150

    svg_elements = []

    svg_elements.append(
        f'<circle cx="{center_x}" cy="{center_y}" r="{radius}" stroke="black" fill="none"/>'
    )

    # Date 1
    for i in range(s1["cycle"]):
        angle = (2 * math.pi / s1["cycle"]) * i
        length = 60 + s1["day"] * 2
        x2 = center_x + length * math.cos(angle)
        y2 = center_y + length * math.sin(angle)

        svg_elements.append(
            f'<line x1="{center_x}" y1="{center_y}" x2="{x2}" y2="{y2}" stroke="blue" stroke-width="2"/>'
        )

    # Date 2 (rotire)
    offset = (s2["month"] / 12) * 2 * math.pi
    for i in range(s2["cycle"]):
        angle = (2 * math.pi / s2["cycle"]) * i + offset
        length = 60 + s2["day"] * 2
        x2 = center_x + length * math.cos(angle)
        y2 = center_y + length * math.sin(angle)

        svg_elements.append(
            f'<line x1="{center_x}" y1="{center_y}" x2="{x2}" y2="{y2}" stroke="red" stroke-width="2"/>'
        )

    harmony_value = abs(s1["total"] - s2["total"])
    harmony_radius = 40 + harmony_value * 2

    svg_elements.append(
        f'<circle cx="{center_x}" cy="{center_y}" r="{harmony_radius}" stroke="purple" fill="none" stroke-dasharray="5,5"/>'
    )

    svg = f"""
    <svg width="400" height="400" viewBox="0 0 400 400"
         xmlns="http://www.w3.org/2000/svg">
        {''.join(svg_elements)}
    </svg>
    """

    return svg

@app.route("/")
def home():
    return """
    <h2>Valentine Harmony Glyph</h2>
    <form action="/download">
        <input name="date1" placeholder="Date 1 (YYYY-MM-DD)" required>
        <input name="date2" placeholder="Date 2 (YYYY-MM-DD)" required>
        <button type="submit">Download PNG</button>
    </form>
    """

@app.route("/download")
def download():
    date1 = request.args.get("date1")
    date2 = request.args.get("date2")

    if not date1 or not date2:
        return "Both dates required"

    svg = generate_svg(date1, date2)

    png_bytes = cairosvg.svg2png(bytestring=svg.encode("utf-8"))

    return send_file(
        io.BytesIO(png_bytes),
        mimetype="image/png",
        as_attachment=True,
        download_name=f"valentine_{date1}_{date2}.png"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
