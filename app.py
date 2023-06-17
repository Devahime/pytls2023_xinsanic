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
    return "BMI calculator"

if __name__ == '__main__':
    app.run(debug=True, port=5000)

@app.route('/home' ,methods=['GET', 'POST'])
def home():
    bmi=None
    bmitype=None
    if request.method == 'POST':
        gender = (request.form['gender'])
        age = float(request.form['age'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        bmi = weight / ((height / 100) ** 2)
        if bmi <= 18.59:
            bmitype="Underweight"
        elif bmi > 18.60 and bmi < 24.99:
            bmitype="Normal"
        elif bmi > 25 and bmi < 29.99:
            bmitype="Overweight"
        elif bmi > 30:
            bmitype="Obese"


    return render_template('index.html', bmi=bmi, bmitype=bmitype)

@app.route('/download-csv')
def download_csv():
    # Nastavte cestu k vašemu CSV souboru
    csv_file = 'bmi.csv'

    # Nastavte název souboru pro stažení
    download_filename = 'bmi.csv'

    return send_file(csv_file, as_attachment=True, attachment_filename=download_filename)

data = [
    ["Gender", 'Age', 'Weight', "Height"],
]

# Nastavte název CSV souboru
csv_file = 'bmi.csv'

# Otevřete CSV soubor pro zápis
with open(csv_file, 'w', newline='') as file:
    writer = csv.writer(file)

    # Zapíšete data do CSV souboru
    writer.writerows(data)

print(f'CSV soubor "{csv_file}" byl vytvořen.')









