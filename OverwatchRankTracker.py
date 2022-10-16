
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import PySimpleGUI as sg
import sys



# new plan: refactor my columns to be more categorical:  each row is one game with the following columns: win/loss/draw, role, map, gameMode, etc...
# also there will be a column for the day's date, or maybe just a column that is how many days in that particular observation is, starting at 1 for the first observation



# the plan: write to an empty file to keep track of wins/losses and every 7 games


''' FUNCTIONS '''

def addrow(gameOutcome, Role):
    try:
        #mydata.loc[len(mydata.index)] = [gameOutcome, Role]
        df = {"Win/Loss/Draw": gameOutcome, "Role": Role}
        return mydata.append(df, ignore_index = True)
    except:
        print("cannot set a row with mismatached columns OR some other error idk")
        







''' READING IN THE EXCEL FILE '''

# reading in the file to a pandas dataframe
mydata = pd.read_excel("OverwatchRankStats.xlsx")



# removes any unwanted columns that may have been created
#mydata = mydata[ ['Win/Loss/Draw', 'Role'] ]    

# making changes to the dataframe 

# if these columns do not exist add them
if ('Win/Loss/Draw' not in mydata.columns):
    mydata['Win/Loss/Draw'] = []
    print("added win/loss/draw")
    
if ('Role' not in mydata.columns):
    mydata['Role'] = []
    print("added role")


''' GETTING USER INPUT '''

layout = [  [sg.Text("Did you win or lose? (click the corresponding box)")], 
            [sg.Button("Win"), sg.Button("Loss"), sg.Exit()] ]
            

InputWindow = sg.Window('Overwatch Stats Program', layout, margins = (100, 100))    

while True: # while the window is active do this
    event, values = InputWindow.read()
    if (event == sg.WIN_CLOSED):
        break
    if (event == 'Exit'):
        InputWindow.close()
        print("exited")
        #sys.exit(0) 
        break
    if (event == 'Win'):
        print("win")
        #mydata.at[0, 'totalWon'] += 1   # just... no
        gameOutcome = "win"
        mydata = addrow('win', 'nan')
        break
    if (event == 'Loss'):
        print("loss")
        #mydata.at[0, 'totalLost'] += 1  # please stop
        gameOutcome = "loss"
        mydata = addrow('loss', 'nan')
        break

# closes the window after the loop breaks
InputWindow.close()



''' CLEANING THE DATA '''

# removes any unwanted columns that may have been created
mydata = mydata[ ['Win/Loss/Draw', 'Role'] ]        








''' CALCULATING AND DISPLAYING STATISTICS '''

# One-hot encoding win/loss/draw 
EncodedData = pd.get_dummies(mydata, columns =["Win/Loss/Draw"], prefix = ["Outcome"])

try:
    Wins = EncodedData["Outcome_win"].sum()
except:
    Wins = 0
    
try:
    Losses = EncodedData["Outcome_loss"].sum()
except:
    Losses = 0

layout = [  [sg.Text("Total games won this season: " + str(Wins) )], 
            [sg.Text("Total games lost this season: " + str(Losses) )], 
            [sg.Button('Close')]]

statsWindow = sg.Window('Stats Window', layout, margins = (100, 100))

while True:
    event, values = statsWindow.read()
    if (event == sg.WIN_CLOSED or event == 'Close'):
        break
    
statsWindow.close()


''' APPLYING CHANGES TO ORIGINAL FILE '''

# applying the dataframe changes to the file
mydata.to_excel("OverwatchRankStats.xlsx")

#mydata = mydata.drop('Observations', 1) # Dropping the observations column. 1 for cols, 0 for rows
#mydata = mydata.drop('Size of holds', 1)
#mydata = mydata.drop('Distance between holds for intended beta', 1)

#tempdata = mydata

#for x in range(25, 29):
    #tempdata = tempdata.drop([mydata.index[x]])
    


    
            

    



