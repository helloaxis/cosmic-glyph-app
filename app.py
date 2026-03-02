from flask import Flask, request, redirect
import os

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h2>Cosmic Glyph Generator</h2>
    <p>App is running successfully.</p>
    """

if __name__ == "__main__":
    app.run()
