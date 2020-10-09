from flask import Flask, render_template, request, redirect
import pandas as pd
import xlsxwriter as xl
from extract_covid_cases import extract
import math


app = Flask(__name__)


states = ['Andaman and Nicobar Islands', 'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh', 'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Jharkhand', 'Karnataka', 'Kerala', 'Ladakh', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal']
unknowns = {"Andaman and Nicobar Islands", "Assam", "Goa", "Manipur", "Sikkim", "Telangana"}


@app.route('/', methods=['GET', 'POST'])
def home():
    global states, unknowns
    if request.method == "GET":
        return render_template("home.html", data=states)
    else:
        data, districts = extract(request.form['state'])
        workbook = xl.Workbook(str(request.form['state']) + ".xlsx")
        bold = workbook.add_format({'bold': True})
        text_wrap = workbook.add_format().set_text_wrap(True)
        state_sheet = workbook.add_worksheet(str(request.form['state']))
        state_sheet.write(0, 0, "Date", bold)
        state_sheet.write(0, 1, "State", bold)
        state_sheet.write(0, 2, "District", bold)
        state_sheet.write(0, 3, "Active", bold)
        state_sheet.write(0, 4, "Confirmed", bold)
        state_sheet.write(0, 5, "Recovered", bold)
        state_sheet.write(0, 6, "Deceased", bold)
        state_sheet.write(0, 7, "Tested", bold)
        if request.form['state'] not in unknowns:
            for district in districts:
                new_sheet = workbook.add_worksheet(district)
                new_sheet.write(0, 0, "Date", bold)
                new_sheet.write(0, 1, "State", bold)
                new_sheet.write(0, 2, "District", bold)
                new_sheet.write(0, 3, "Active", bold)
                new_sheet.write(0, 4, "Confirmed", bold)
                new_sheet.write(0, 5, "Recovered", bold)
                new_sheet.write(0, 6, "Deceased", bold)
                new_sheet.write(0, 7, "Tested", bold)
                district_data = data.loc[(data[2] == district)]
                row = 1
                for index, covid_data in district_data.iterrows():
                    print(covid_data[0], covid_data[1], covid_data[2], str(covid_data[3]), str(covid_data[4]), str(covid_data[5]), str(covid_data[7]))
                    new_sheet.write(row, 0, covid_data[0], text_wrap)
                    new_sheet.write(row, 1, covid_data[1], text_wrap)
                    new_sheet.write(row, 2, covid_data[2], text_wrap)
                    if str(covid_data[3]) != "nan":
                        new_sheet.write(row, 4, str(covid_data[3]), text_wrap)
                    if str(covid_data[4]) != "nan":
                        new_sheet.write(row, 5, str(covid_data[4]), text_wrap)
                    if str(covid_data[5]) != "nan":
                        new_sheet.write(row, 6, str(covid_data[5]), text_wrap)
                    if str(covid_data[7]) != "nan":
                        new_sheet.write(row, 7, str(covid_data[7]), text_wrap)
                    row += 1
        workbook.close()
        return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True, port='8080')
