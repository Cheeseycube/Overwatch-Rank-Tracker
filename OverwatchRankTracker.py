
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

# IMPORTING AND CLEANING THE DATA
mydata = pd.read_excel("OverwatchRankStats")


mydata = mydata.drop('Observations', 1) # Dropping the observations column. 1 for cols, 0 for rows
mydata = mydata.drop('Size of holds', 1)
mydata = mydata.drop('Distance between holds for intended beta', 1)

tempdata = mydata

for x in range(25, 29):
    tempdata = tempdata.drop([mydata.index[x]])
    

tempdata = tempdata.fillna(0)    
mis_val = tempdata.isnull().sum()
mydata = tempdata
    
    



