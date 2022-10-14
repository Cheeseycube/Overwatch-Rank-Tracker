
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import PySimpleGUI as sg
import sys

# the plan: write to an empty file to keep track of wins/losses and every 7 games

# reading in the file to a pandas dataframe
mydata = pd.read_excel("OverwatchRankStats.xlsx")



# making changes to the dataframe 

# if these columns do not exist add them
if ('totalLost' not in mydata.columns):
    mydata['totalLost'] = [];
    
if ('totalWon' not in mydata.columns):
    mydata['totalWon'] = [];


'''Getting user input'''
numJugs = 0

layout = [  [sg.Text("Did you win or lose? (click the corresponding box)")], 
            [sg.Button("Win"), sg.Button("Loss")], 
            sg.Exit() ]

InputWindow = sg.Window('Overwatch Stats Program', layout, margins = (100, 100))    

while True: # basically a switch statement that exits on break
    event, values = InputWindow.read()
    if (event == sg.WIN_CLOSED):
        break
    if (event == 'Exit'):
        InputWindow.close()
        print("exited")
        sys.exit(0) 
        break
    if (event == 'Submit'):
        print("submitted")
        break

# closes the window after the loop breaks
InputWindow.close()

# checking if input is an integer
try:
    numJugs = int(values[0])
except:
    numJugs = f"invalid entry: {values[0]}"
sg.popup('You entered', numJugs)



print(f"{numJugs} is what the user typed")














# applying the dataframe changes to the file
mydata.to_excel("OverwatchRankStats.xlsx")

#mydata = mydata.drop('Observations', 1) # Dropping the observations column. 1 for cols, 0 for rows
#mydata = mydata.drop('Size of holds', 1)
#mydata = mydata.drop('Distance between holds for intended beta', 1)

#tempdata = mydata

#for x in range(25, 29):
    #tempdata = tempdata.drop([mydata.index[x]])
    
# any missing values?
mydata = mydata.fillna(0)    
mis_val = mydata.isnull().sum()



    



