from flask import Flask
from algo import *
from rob import *
import csv

app =  Flask(__name__)

@app.route("/")
def hello_world():
    exec(open('algo.py').read())
    return str(predicted_number)


app.run(host="0.0.0.0", port=5067)



