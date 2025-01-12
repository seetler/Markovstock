from flask import Flask
from algo import *
from rob import *

app =  Flask(__name__)

@app.route("/")
def hello_world():
    return "xd sl"

app.run(host="0.0.0.0", port=5067)