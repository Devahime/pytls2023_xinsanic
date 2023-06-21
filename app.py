from pywebio.input import *
from pywebio.output import *
from flask import Flask, render_template, request, send_file, send_from_directory
import os
import matplotlib
from matplotlib import cm
from matplotlib import pyplot as plt
import numpy as np
import csv
from gauge import gauge

app = Flask(__name__)

@app.route("/")
def index():
    return '<a href="http://127.0.0.1:5000/home"> BMI calculator</a>'

if __name__ == '__main__':
    app.run(debug=True, port=5000)

def write_entry(gender: str, age: int, height: float, weight: float, bmi: float):

    write_header = os.path.exists("data.csv") == False

    with open("data.csv", "a+") as file:
        writer = csv.writer(file, delimiter=";",
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
        if write_header:
            writer.writerow([
                'gender',
                'age',
                'height',
                'weight',
                'bmi'
            ])

        writer.writerow([
            gender, age, height, weight, bmi
        ])

def read_entries() -> list[dict[str, float | int | str]]:
    #Read entries from data.csv

    entries: list[dict[str, float | int | str]] = []

    if os.path.exists("data.csv"):

        with open("data.csv", "r") as file:
            reader = csv.reader(file, delimiter=";")

            for entry in reader:
                if len(entry) == 0 or entry[0] == 'gender':
                    continue

                entries.append({
                    'gender': entry[0],
                    'age': int(entry[1]),
                    'height': float(entry[2]),
                    'weight': float(entry[3]),
                    'bmi': float(entry[4])
                })

    return entries

@app.route("/download-csv", methods=['GET', 'POST'])
def download_csv():
    return send_from_directory(app.root_path, "data.csv")
@app.route('/home' ,methods=['GET', 'POST'])
def home():
    bmi=None
    bmitype=None
    bmitext=None

    if request.method == 'POST':
        gender = (request.form['gender'])
        age = int(request.form['age'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        bmi = weight / ((height / 100) ** 2)

        if bmi <= 18.50:
            bmitype="Underweight"
            bmitext ="Being underweight can have negative implications for overall health, including reduced energy levels, weakened immune function, and an increased risk of bone and muscle issues. If you receive an underweight BMI result, it is important to consult with a healthcare professional who can provide personalized guidance and support to help you achieve a healthy weight and improve your overall well-being."
        elif bmi > 18.50 and bmi <= 25:
            bmitype="Normal"
            bmitext="Having a normal BMI is often associated with several positive health outcomes. It suggests that an individual has a balanced body weight, which can contribute to overall well-being and a reduced risk of certain health conditions."
        elif bmi > 25 and bmi <= 30:
            bmitype="Overweight"
            bmitext="Being overweight can result from various factors, including excessive caloric intake, lack of physical activity, genetic factors, hormonal imbalances, or certain medical conditions. It is important to note that being overweight can have negative implications for overall health and well-being."
        elif bmi > 30:
            bmitype="Obese"
            bmitext="Being obese can result from a combination of factors, including excessive caloric intake, sedentary lifestyle, genetic predisposition, hormonal imbalances, and certain medical conditions. It is important to note that obesity can have serious implications for overall health and well-being."

        past_quote = None
        entries = read_entries()

        if len(entries) > 1:
            last_entry = entries[len(entries) - 1]
            if float(last_entry['bmi']) > bmi:
                past_quote = "You're improving, keep it up!"
            else:
                past_quote = "You're slacking,.. better start doing something with your life..."

        #ulozeni do csv
        write_entry(gender, age, height, weight, bmi)

        values = {
            'gender': gender,
            'age': age,
            'height': height,
            'weight': weight,
        }

        fig = gauge(bmi,
                    labels=['Underweight', 'Normal', 'Overweight', 'Obese'],
                    ranges=[
                        0,
                        18.6,
                        25,
                        30,
                        48.6
                    ],
                    colors=['#007A00', '#0063BF', '#FFCC00', '#ED1C24'],
                    bg_color='#e3d0fc')

        plt.savefig('./static/images/graph.png')
        return render_template('index.html',
                                bmi=bmi,
                                bmitype=bmitype,
                                bmitext=bmitext,
                                values=values,
                                past_quote=past_quote,
                                plot=True
                                )

    return render_template('index.html', bmi=bmi, bmitype=bmitype, bmitext=bmitext)
