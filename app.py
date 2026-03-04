from flask import Flask, request
from openai import OpenAI
import os
import base64

app = Flask(__name__)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def reducere(n):
    while n > 9:
        n = sum(int(c) for c in str(n))
    return n

def analiza_data(data_str):
    zi = reducere(int(data_str[:2]))
    luna = reducere(int(data_str[3:5]))
    an = reducere(sum(int(c) for c in data_str[6:]))
    return reducere(zi + luna + an)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        d1 = request.form["data1"]
        d2 = request.form["data2"]

        N1 = analiza_data(d1)
        N2 = analiza_data(d2)
        U = reducere(N1 + N2)

        prompt = f"""
        Create a unique sacred geometric cosmic glyph.

        Left energy number: {N1}
        Right energy number: {N2}
        Union number: {U}

        Style: Deep Indigo Nebula
        Luminous sacred geometry, symmetrical, deep space background,
        cinematic lighting, ultra high resolution, premium artwork.
        """

        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            size="1024x1024"
        )

        image_base64 = result.data[0].b64_json

        return f"""
        <h2>Your Cosmic Glyph</h2>
        <img src="data:image/png;base64,{image_base64}" />
        <br><br>
        <a href="/">Generate Another</a>
        """

    return """
    <h2>Cosmic Glyph Generator</h2>
    <form method="POST">
        First date (dd.mm.yyyy):<br>
        <input name="data1" required><br><br>
        Second date (dd.mm.yyyy):<br>
        <input name="data2" required><br><br>
        <button type="submit">Generate Glyph</button>
    </form>
    """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
