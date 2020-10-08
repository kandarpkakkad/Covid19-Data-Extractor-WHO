from flask import Flask, render_template, request
import pandas as pd
from extract_covid_cases import extract


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "GET":
        return render_template("home.html")
    else:
        data, districts = extract(request.form['state'])
        return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True, port='8080')
