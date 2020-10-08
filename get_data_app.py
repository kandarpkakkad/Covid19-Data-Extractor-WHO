from flask import Flask, render_template, request
import pandas as pd
from extract_covid_cases import extract


app = Flask(__name__)


states = ['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']


@app.route('/', methods=['GET', 'POST'])
def home():
    global states
    if request.method == "GET":
        return render_template("home.html", data=states)
    else:
        data, districts = extract(request.form['state'])
        return render_template("home.html")


if __name__ == "__main__":
    app.run(debug=True, port='8080')
