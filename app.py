from pywebio.input import *
from pywebio.output import *
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return "BMI calculator"

if __name__ == '__main__':
    app.run(debug=True, port=5000)

@app.route('/home' ,methods=['GET', 'POST'])
def home():
    bmi=None
    if request.method == 'POST':
        gender = (request.form['gender'])
        age = float(request.form['age'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        bmi = weight / ((height / 100) ** 2)
        if bmi <= 18,59:
            print(Underweight)
    return render_template('index.html', bmi=bmi)



