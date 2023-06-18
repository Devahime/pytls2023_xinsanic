from pywebio.input import *
from pywebio.output import *
from flask import Flask, render_template, request, send_file
import os, sys
import matplotlib
from matplotlib import cm
from matplotlib import pyplot as plt
import numpy as np
import csv

app = Flask(__name__)

@app.route("/")
def index():
    return '<a href="http://127.0.0.1:5000/home"> BMI calculator</a>'

if __name__ == '__main__':
    app.run(debug=True, port=5000)

@app.route('/home' ,methods=['GET', 'POST'])
def home():
    bmi=None
    bmitype=None
    bmitext=None
    if request.method == 'POST':
        gender = (request.form['gender'])
        age = float(request.form['age'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        bmi = weight / ((height / 100) ** 2)
        if bmi <= 18.59:
            bmitype="Underweight"
            bmitext ="Being underweight can have negative implications for overall health, including reduced energy levels, weakened immune function, and an increased risk of bone and muscle issues. If you receive an underweight BMI result, it is important to consult with a healthcare professional who can provide personalized guidance and support to help you achieve a healthy weight and improve your overall well-being."
        elif bmi > 18.60 and bmi < 24.99:
            bmitype="Normal"
        elif bmi > 25 and bmi < 29.99:
            bmitype="Overweight"
        elif bmi > 30:
            bmitype="Obese"

    return render_template('index.html', bmi=bmi, bmitype=bmitype, bmitext=bmitext)










