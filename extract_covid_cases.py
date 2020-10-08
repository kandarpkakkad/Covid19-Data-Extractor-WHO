import pandas as pd

data2 = pd.DataFrame(pd.read_csv("https://api.covid19india.org/csv/latest/districts.csv", header=None, usecols=[0, 1, 2, 3, 4, 5, 7], low_memory=False))
data2_guj = data2.loc[(data2[1] == "Gujarat") & (data2[2] == "Rajkot")]

print(data2_guj)
