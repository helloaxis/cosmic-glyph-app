
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



       
    """

if __name__ == "__main__":
    port = int(os.environ.get(
