import pandas as pd
import numpy as np
from pandas import read_csv
from matplotlib import pyplot

url="https://raw.githubusercontent.com/SilverWWW/SilverWWW-OR-Hospital-Payment-Records-2018/main/2018%20Hospital%20Payment%20Report%20data.csv"

names = ['Service category','Procedure','Statewide indicator','Hospital','Number of discharges 2018',\
'25th percentile 2018','Median 2018', '75th percentile 2018','Number of discharges 2017','25th percentile 2017',\
'Median 2017','75th percentile 2017','Difference in medians','Percent difference from 2017']

df = pd.read_csv(url)
print(df)   
