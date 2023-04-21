from pywebio.input import *
from pywebio.output import *
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return "This is homepage of my amazing project"

if __name__ == '__main__':
    app.run(debug=True, port=5000)

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/bmicalc', methods=['POST'])
def bmicalc():
    gender = (request.form['gender'])
    woman = (request.form['woman'])
    man = (request.form['man'])
    other = (request.form['other'])
    age = float(request.form['age'])
    height = float(request.form['height'])
    weight = float(request.form['weight'])
    bmi = weight / ((height / 100) ** 2)
    return bmi
