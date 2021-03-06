"""
Covid-19 Data Extractor.

This is a personal project to help people to get data automatically. You need to select the state from the dropdown and
click on submit. You will get an excel sheet for downloading and that will contain the data of the state selected and
all the districts, if any, in that state in different sheets in the file.

The data is extracted from https://www.covid19india.org. This website has its own API, https://api.covid19india.org.
The API contains state-wise, district-wise and whole country's COVID19 data with dates. The excel sheet is generated
using this data.
"""

from flask import Flask, render_template, request, send_from_directory
import xlsxwriter as xl
import pandas as pd
from apscheduler.schedulers.background import BackgroundScheduler


# States and UTs
states = [
    'Andaman and Nicobar Islands',
    'Andhra Pradesh',
    'Arunachal Pradesh',
    'Assam',
    'Bihar',
    'Chandigarh',
    'Chhattisgarh',
    'Dadra and Nagar Haveli and Daman and Diu',
    'Delhi',
    'Goa',
    'Gujarat',
    'Haryana',
    'Himachal Pradesh',
    'Jammu and Kashmir',
    'Jharkhand', 'Karnataka',
    'Kerala',
    'Ladakh',
    'Madhya Pradesh',
    'Maharashtra',
    'Manipur',
    'Meghalaya',
    'Mizoram',
    'Nagaland',
    'Odisha',
    'Puducherry',
    'Punjab',
    'Rajasthan',
    'Sikkim',
    'Tamil Nadu',
    'Telangana',
    'Tripura',
    'Uttar Pradesh',
    'Uttarakhand',
    'West Bengal'
]
# States or UTs which does not have districts
unknowns = [
    "Andaman and Nicobar Islands",
    "Assam",
    "Goa",
    "Manipur",
    "Sikkim",
    "Telangana"
]


# Create Utility Functions
def extract(state: str) -> (pd.DataFrame, list):
    """
    Extractor utility.

    :param state: Name of the state for extraction of the data for the state

    Getting data of respective state and its districts date wise.

    :return: Dataframe of data of respective state
    """
    global unknowns
    try:
        assert isinstance(state, str)
    except AssertionError as _:
        print("String Needed")
        raise
    print("Reading Data for districts of {}".format(state))
    # Read CSV file from covid19india API
    if state in unknowns:
        data_districts = pd.read_csv("https://api.covid19india.org/csv/latest/districts.csv", header=None,
                                     usecols=[0, 1, 3, 4, 5, 7], low_memory=False)
    else:
        data_districts = pd.read_csv("https://api.covid19india.org/csv/latest/districts.csv", header=None,
                                     usecols=[0, 1, 2, 3, 4, 5, 7], low_memory=False)
    # Get data of respective state
    data_districts_state = data_districts.loc[(data_districts[1] == state)]
    districts = []
    if state not in unknowns:
        districts = data_districts_state[2].unique()
    districts.sort()
    return data_districts_state, districts


def extract_state_data(state: str) -> pd.DataFrame:
    """
    State data utility.

    :param state: Name of the state for extraction of the data for the state

    Getting data of respective state date wise.

    :return: Dataframe of data of respective state
    """
    try:
        assert isinstance(state, str)
    except AssertionError as _:
        print("String Needed")
        raise
    print("Reading Data for {}".format(state))
    data = pd.read_csv("https://api.covid19india.org/csv/latest/states.csv", header=None, usecols=[0, 1, 2, 3, 4, 6],
                       low_memory=False)
    return data


schedule = BackgroundScheduler()


def update_data() -> None:
    """
    Update data utility.

    This function will run everyday at midnight and update the data.

    :return: None
    """
    print("[X] Data Retrieval Started...")
    for state in states:
        workbook = xl.Workbook(state[:31] + ".xlsx")
        bold = workbook.add_format({'bold': True, 'font_size': 16})
        text_wrap = workbook.add_format({'text_wrap': True, 'font_size': 13})
        state_sheet = workbook.add_worksheet(state[:31])
        state_sheet.set_column(0, 0, 15)
        state_sheet.set_column(1, 1, len(state) + 5)
        state_sheet.set_column(2, 9, len("Total Confirmed") + 8)
        state_sheet.write(0, 0, "Date", bold)
        state_sheet.write(0, 1, "State", bold)
        state_sheet.write(0, 2, "Daily Confirmed", bold)
        state_sheet.write(0, 3, "Daily Recovered", bold)
        state_sheet.write(0, 4, "Daily Deceased", bold)
        state_sheet.write(0, 5, "Daily Tested", bold)
        state_sheet.write(0, 6, "Total Confirmed", bold)
        state_sheet.write(0, 7, "Total Recovered", bold)
        state_sheet.write(0, 8, "Total Deceased", bold)
        state_sheet.write(0, 9, "Total Tested", bold)
        state_data = extract_state_data(state)
        state_data = state_data.loc[(state_data[1] == state)]
        state_row = 1
        for i in range(len(state_data)):
            state_sheet.write(state_row, 0, state_data.iloc[i, 0], text_wrap)
            state_sheet.write(state_row, 1, state_data.iloc[i, 1], text_wrap)
            if i != 0:
                if str(state_data.iloc[i, 2]) != "nan" and str(state_data.iloc[i - 1, 2]) != "nan":
                    state_sheet.write(state_row, 2, str(int(state_data.iloc[i, 2]) - int(state_data.iloc[i - 1, 2])),
                                      text_wrap)
                elif str(state_data.iloc[i, 2]) != "nan":
                    state_sheet.write(state_row, 2, str(state_data.iloc[i, 2]), text_wrap)
                if str(state_data.iloc[i, 3]) != "nan" and str(state_data.iloc[i - 1, 3]) != "nan":
                    state_sheet.write(state_row, 3, str(int(state_data.iloc[i, 3]) - int(state_data.iloc[i - 1, 3])),
                                      text_wrap)
                elif str(state_data.iloc[i, 3]) != "nan":
                    state_sheet.write(state_row, 3, str(state_data.iloc[i, 3]), text_wrap)
                if str(state_data.iloc[i, 4]) != "nan" and str(state_data.iloc[i - 1, 4]) != "nan":
                    state_sheet.write(state_row, 4, str(int(state_data.iloc[i, 4]) - int(state_data.iloc[i - 1, 4])),
                                      text_wrap)
                elif str(state_data.iloc[i, 4]) != "nan":
                    state_sheet.write(state_row, 4, str(state_data.iloc[i, 4]), text_wrap)
                if str(state_data.iloc[i, 5]) != "nan" and str(state_data.iloc[i - 1, 5]) != "nan":
                    state_sheet.write(state_row, 5, str(int(state_data.iloc[i, 5]) - int(state_data.iloc[i - 1, 5])),
                                      text_wrap)
                elif str(state_data.iloc[i, 5]) != "nan":
                    state_sheet.write(state_row, 5, str(state_data.iloc[i, 5]), text_wrap)
            else:
                if str(state_data.iloc[i, 2]) != "nan":
                    state_sheet.write(state_row, 2, str(state_data.iloc[i, 2]), text_wrap)
                if str(state_data.iloc[i, 3]) != "nan":
                    state_sheet.write(state_row, 3, str(state_data.iloc[i, 3]), text_wrap)
                if str(state_data.iloc[i, 4]) != "nan":
                    state_sheet.write(state_row, 4, str(state_data.iloc[i, 4]), text_wrap)
                if str(state_data.iloc[i, 5]) != "nan":
                    state_sheet.write(state_row, 5, str(state_data.iloc[i, 5]), text_wrap)
            if str(state_data.iloc[i, 2]) != "nan":
                state_sheet.write(state_row, 6, str(state_data.iloc[i, 2]), text_wrap)
            if str(state_data.iloc[i, 3]) != "nan":
                state_sheet.write(state_row, 7, str(state_data.iloc[i, 3]), text_wrap)
            if str(state_data.iloc[i, 4]) != "nan":
                state_sheet.write(state_row, 8, str(state_data.iloc[i, 4]), text_wrap)
            if str(state_data.iloc[i, 5]) != "nan":
                state_sheet.write(state_row, 9, str(state_data.iloc[i, 5]), text_wrap)
            state_row += 1
        if state not in unknowns:
            data, districts = extract(state)
            for district in districts:
                worksheets = workbook.get_worksheet_by_name(district[:31])
                if worksheets is None:
                    new_sheet = workbook.add_worksheet(district[:31])
                else:
                    new_sheet = workbook.add_worksheet(district[:30] + "_dist")
                new_sheet.set_column(0, 0, 15)
                new_sheet.set_column(1, 1, len(state) + 5)
                new_sheet.set_column(2, 2, len(district) + 5)
                new_sheet.set_column(3, 10, len("Total Confirmed") + 8)
                new_sheet.write(0, 0, "Date", bold)
                new_sheet.write(0, 1, "State", bold)
                new_sheet.write(0, 2, "District", bold)
                new_sheet.write(0, 3, "Daily Confirmed", bold)
                new_sheet.write(0, 4, "Daily Recovered", bold)
                new_sheet.write(0, 5, "Daily Deceased", bold)
                new_sheet.write(0, 6, "Daily Tested", bold)
                new_sheet.write(0, 7, "Total Confirmed", bold)
                new_sheet.write(0, 8, "Total Recovered", bold)
                new_sheet.write(0, 9, "Total Deceased", bold)
                new_sheet.write(0, 10, "Total Tested", bold)
                district_data = data.loc[(data[2] == district)]
                row = 1
                for i in range(len(district_data)):
                    new_sheet.write(row, 0, district_data.iloc[i, 0], text_wrap)
                    new_sheet.write(row, 1, district_data.iloc[i, 1], text_wrap)
                    new_sheet.write(row, 2, district_data.iloc[i, 2], text_wrap)
                    if i != 0:
                        if str(district_data.iloc[i, 3]) != "nan" and str(district_data.iloc[i - 1, 3]) != "nan":
                            new_sheet.write(row, 3, str(int(district_data.iloc[i, 3]) - int(district_data.iloc[i - 1,
                                                                                                               3])),
                                            text_wrap)
                        elif str(district_data.iloc[i, 3]) != "nan":
                            new_sheet.write(row, 3, str(district_data.iloc[i, 3]), text_wrap)
                        if str(district_data.iloc[i, 4]) != "nan" and str(district_data.iloc[i - 1, 4]) != "nan":
                            new_sheet.write(row, 4, str(int(district_data.iloc[i, 4]) - int(district_data.iloc[i - 1,
                                                                                                               4])),
                                            text_wrap)
                        elif str(district_data.iloc[i, 4]) != "nan":
                            new_sheet.write(row, 4, str(district_data.iloc[i, 4]), text_wrap)
                        if str(district_data.iloc[i, 5]) != "nan" and str(district_data.iloc[i - 1, 5]) != "nan":
                            new_sheet.write(row, 5, str(int(district_data.iloc[i, 5]) - int(district_data.iloc[i - 1,
                                                                                                               5])),
                                            text_wrap)
                        elif str(district_data.iloc[i, 5]) != "nan":
                            new_sheet.write(row, 5, str(district_data.iloc[i, 5]), text_wrap)
                        if str(district_data.iloc[i, 6]) != "nan" and str(district_data.iloc[i - 1, 6]) != "nan":
                            new_sheet.write(row, 6, str(int(district_data.iloc[i, 6]) - int(district_data.iloc[i - 1,
                                                                                                               6])),
                                            text_wrap)
                        elif str(district_data.iloc[i, 6]) != "nan":
                            new_sheet.write(row, 6, str(district_data.iloc[i, 6]), text_wrap)
                    else:
                        if str(district_data.iloc[i, 3]) != "nan":
                            new_sheet.write(row, 3, str(district_data.iloc[i, 3]), text_wrap)
                        if str(district_data.iloc[i, 4]) != "nan":
                            new_sheet.write(row, 4, str(district_data.iloc[i, 4]), text_wrap)
                        if str(district_data.iloc[i, 5]) != "nan":
                            new_sheet.write(row, 5, str(district_data.iloc[i, 5]), text_wrap)
                        if str(district_data.iloc[i, 6]) != "nan":
                            new_sheet.write(row, 6, str(district_data.iloc[i, 6]), text_wrap)
                    if str(district_data.iloc[i, 3]) != "nan":
                        new_sheet.write(row, 7, str(district_data.iloc[i, 3]), text_wrap)
                    if str(district_data.iloc[i, 4]) != "nan":
                        new_sheet.write(row, 8, str(district_data.iloc[i, 4]), text_wrap)
                    if str(district_data.iloc[i, 5]) != "nan":
                        new_sheet.write(row, 9, str(district_data.iloc[i, 5]), text_wrap)
                    if str(district_data.iloc[i, 6]) != "nan":
                        new_sheet.write(row, 10, str(district_data.iloc[i, 6]), text_wrap)
                    row += 1
        workbook.close()
    print("[X] Data Retrieval Completed...")


schedule.add_job(update_data, trigger="cron", day_of_week='mon-sun', hour=22, minute=30, end_date='2060-12-31')
schedule.start()


# Create Flask App
app = Flask(__name__)


# Route 1 --> Home Route
@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Home route.

    This is home route.

    :return: HTML page or excel file
    """
    global states, unknowns
    if request.method == "GET":
        return render_template("home.html", data=states)
    else:
        return send_from_directory(directory="", filename=request.form['state'][:31] + ".xlsx", as_attachment=True)


@app.route("/about", methods=['GET'])
def about():
    """
    About page.

    :return: HTML page
    """
    return render_template("about.html")


@app.route("/contact", methods=['GET'])
def contact():
    """
    Contact page.

    :return: HTML page
    """
    return render_template("contact.html")


@app.errorhandler(404)
def not_found(_):
    """
    Page Not Found page.

    :return: HTML page
    """
    return render_template("404.html")


if __name__ == "__main__":
    app.run(debug=True)
else:
    schedule.shutdown()
