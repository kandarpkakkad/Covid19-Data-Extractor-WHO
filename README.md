# Covid19-Data-Extractor-WHO

```
Retrieves Covid-19 Updates from api.covid19india.org API and creates excel sheet for state and district wise timeline data
```

## Introduction

This is a personal project to help WHO employees to get data automatically. You need to select the state from the dropdown and click on submit. You will get an excel sheet for downloading and that will contain the data of the state selected and all the districts, if any, in that state in different sheets in the file.

The data is extracted from https://www.covid19india.org. This website has its own API, https://api.covid19india.org. The API contains state-wise, district-wise and whole country's COVID19 data with dates. The excel sheet is generated using this data.

## Techonology

The project uses Flask for backend and Jinja2 templates for frontend. XlsxWriter library is used to write in excel file.

#### 1. Flask

```python
from flask import Flask, render_template, request, send_from_directory
import xlsxwriter as xl
import pandas as pd
```

We extract the district data and state data using the utility functions below

```python
def extract(state: str) -> (pd.DataFrame, list):
    """
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
        data_districts = pd.read_csv("https://api.covid19india.org/csv/latest/districts.csv", header=None, usecols=[0, 1, 3, 4, 5, 7], low_memory=False)
    else:
        data_districts = pd.read_csv("https://api.covid19india.org/csv/latest/districts.csv", header=None, usecols=[0, 1, 2, 3, 4, 5, 7], low_memory=False)
    # Get data of respective state
    data_districts_state = data_districts.loc[(data_districts[1] == state)]
    districts = []
    if state not in unknowns:
        districts = data_districts_state[2].unique()
    districts.sort()
    return data_districts_state, districts

def extract_state_data(state: str) -> pd.DataFrame:
    """
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
    data = pd.read_csv("https://api.covid19india.org/csv/latest/states.csv", header=None, usecols=[0, 1, 2, 3, 4, 6], low_memory=False)
    return data
```

#### 2. Jinja Templates

We have a common template that is used by all the pages.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" name="viewport" content="width=device-width, initial-scale=1">
    <title></title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js"></script>
</head>
<body class="bg-dark">
    <nav class="navbar navbar-expand-md bg-dark navbar-dark">
        <div class="container">
            <a class="navbar-brand" href="/">Covid Data Extractor</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target=".navbar-collapse">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="collapsibleNavbar">
                <ul class="navbar-nav  ml-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/about">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/contact">Contact</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="d-flex justify-content-center align-items-center" style="height: 80vh">
    {% block content %}
    {% endblock %}
    </div>

    <footer class="page-footer fixed-bottom bg-dark text-white">
        <div class="footer-copyright text-center py-3">© 2020 Copyright:
            <a href="https://api.covid19india.org/" class="text-white"> https://api.covid19india.org/</a>
        </div>
    </footer>

</body>
</html>
```
