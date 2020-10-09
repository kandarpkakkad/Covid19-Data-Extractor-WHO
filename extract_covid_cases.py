import pandas as pd


def extract(state: str) -> (pd.DataFrame, list):
    """
    :param state: Name of the state for extraction of the data for the state

    Getting data of respective state and its districts date wise.

    :return: Dataframe of data of respective state
    """
    try:
        assert isinstance(state, str)
    except AssertionError as _:
        print("String Needed")
        raise
    print("Reading Data for {}".format(state))
    unknowns = {"Andaman and Nicobar Islands", "Assam", "Goa", "Manipur", "Sikkim", "Telangana"}
    # Read CSV file from covid19india API
    if state in unknowns:
        data_districts = pd.read_csv("https://api.covid19india.org/csv/latest/districts.csv", header=None,
                                     usecols=[0, 1, 3, 4, 5, 7])
    else:
        data_districts = pd.read_csv("https://api.covid19india.org/csv/latest/districts.csv", header=None,
                                     usecols=[0, 1, 2, 3, 4, 5, 7])
    # Get data of respective state
    data_districts_state = data_districts.loc[(data_districts[1] == state)]
    districts = []
    if state not in unknowns:
    	districts = data_districts_state[2].unique()
    print(data_districts_state, districts)
    return data_districts_state, districts
