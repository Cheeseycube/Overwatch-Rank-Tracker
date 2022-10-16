
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import PySimpleGUI as sg
import sys

gameOutcome = "nan"
Role = "nan"
# new plan: refactor my columns to be more categorical:  each row is one game with the following columns: win/loss/draw, role, map, gameMode, etc...
# also there will be a column for the day's date, or maybe just a column that is how many days in that particular observation is, starting at 1 for the first observation



# the plan: write to an empty file to keep track of wins/losses and every 7 games


''' FUNCTIONS '''

def addrow():
    try:
        #mydata.loc[len(mydata.index)] = [gameOutcome, Role]
        df = {"Win/Loss/Draw": gameOutcome, "Role": Role}
        return mydata.append(df, ignore_index = True)
    except:
        print("cannot set a row with mismatached columns OR some other error idk")
        
def createTankdata():
    Tankdata = EncodedData
    for i in EncodedData.index:
        if (EncodedData["Role"][i] != "tank"):
            Tankdata = Tankdata.drop([EncodedData.index[i]])
    return Tankdata





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

layout = [  [sg.Text("Did you win or lose? (click the corresponding box)", font = ("Helvetica", 20) )], 
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
        break
    if (event == 'Loss'):
        print("loss")
        #mydata.at[0, 'totalLost'] += 1  # please stop
        gameOutcome = "loss"
        break

# closes the window after the loop breaks
InputWindow.close()




layout = [  [sg.Text("What role did you play as?", font = ("Helvetica", 20) )], 
            [sg.Button("Tank"), sg.Button("Support"), sg.Button("Damage"), sg.Exit()] ]
            

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
    if (event == 'Tank'):
        print("tank")
        Role = "tank"
        break
    if (event == 'Support'):
        print("Support")
        Role = "support"
        break
    if (event == 'Damage'):
        print("Damage")
        Role = "damage"
        break

# closes the window after the loop breaks
InputWindow.close()

mydata = addrow()   # this could be problematic if we just want to view statistics

# to curb the above problem, there should be a button that brings up stats so you can see them without making changes


''' CLEANING THE DATA '''

# removes any unwanted columns that may have been created
mydata = mydata[ ['Win/Loss/Draw', 'Role'] ]        








''' CALCULATING AND DISPLAYING STATISTICS '''

# One-hot encoding win/loss/draw 
EncodedData = pd.get_dummies(mydata, columns =["Win/Loss/Draw"], prefix = ["Outcome"])
Tankdata = createTankdata()

# could use 'if outcomewin in columns' instead of try except I think?

    
if ('Outcome_win' in EncodedData.columns):
    Wins = EncodedData["Outcome_win"].sum()
else:
    Wins = 0
    
if ('Outcome_loss' in EncodedData.columns):
    Losses = EncodedData["Outcome_loss"].sum()
else:
    Losses = 0

# if statements may be unneccessary here
if ('Outcome_win' in Tankdata.columns):
    Tank_Wins = Tankdata["Outcome_win"].sum()
else:
    Tank_Wins = 0
    
if ('Outcome_loss' in Tankdata.columns):
    Tank_Losses = Tankdata["Outcome_loss"].sum()
else:
    Tank_Losses = 0



# could use f-strings here instead of concatenation?

layout = [  [sg.Text("Total games won this season: " + str(Wins), font = ("Helvetica", 20) )], # trying font stuff
            [sg.Text("Total games lost this season: " + str(Losses), font = ("Helvetica", 20) )],
            [sg.Text("Total games won on tank this season: " + str(Tank_Wins), font = ("Helvetica", 20) )],
            [sg.Text("Total games lost on tank this season: " + str(Tank_Losses), font = ("Helvetica", 20) )],
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


    


    
            

    



