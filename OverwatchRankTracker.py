import pandas as pd
import numpy as np
import PySimpleGUI as sg
import sys


# gameOutcome = "nan" Role = "nan" new plan: refactor my columns to be more categorical:  each row is one game with
# the following columns: win/loss/draw, role, map, gameMode, etc... also there will be a column for the day's date,
# or maybe just a column that is how many days in that particular observation is, starting at 1 for the first
# observation estimate ranking?


# the plan: write to an empty file to keep track of wins/losses and every 7 games


''' FUNCTIONS '''

def addrow(gameOutcome, role, givendata):
    try:
        #givendata.loc[len(givendata.index)] = [gameOutcome, role]
        newRow = {"Win/Loss/Draw": gameOutcome, "Role": role}
        return givendata.append(newRow, ignore_index=True)
    except:
        print("cannot set a row with mismatched columns OR some other error idk")


def createTankdata(EncodedData):
    Tankdata = EncodedData
    for i in EncodedData.index:
        if (EncodedData["Role"][i] != "Tank"):
            Tankdata = Tankdata.drop([EncodedData.index[i]])
    return Tankdata


def displayStats(givenData):
    # Calculating Statistics
    EncodedData = pd.get_dummies(givenData, columns=["Win/Loss/Draw"], prefix=["Outcome"])
    Tankdata = createTankdata(EncodedData)

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

    # displaying stats
    layout = [[sg.Text("Total games won this season: " + str(Wins), font=("Helvetica", 20))],  # trying font stuff
              [sg.Text("Total games lost this season: " + str(Losses), font=("Helvetica", 20))],
              [sg.Text("Total games won on tank this season: " + str(Tank_Wins), font=("Helvetica", 20))],
              [sg.Text("Total games lost on tank this season: " + str(Tank_Losses), font=("Helvetica", 20))],
              [sg.Button('Close')]]

    statsWindow = sg.Window('Stats Window', layout, margins=(100, 100))

    while True:
        event, values = statsWindow.read()
        if (event == sg.WIN_CLOSED or event == 'Close'):
            statsWindow.close()
            sys.exit(0)
            break

    statsWindow.close()


def addGame(givendata):
    gameOutcome = "win"     # default value--based off the gui
    role = "Tank"           # default value--based off the gui
                                            # row 1
    layout = [[sg.Text("Please fill out the following information:", font=("Helvetica", 40))],
                                            # row 2
              [sg.Radio("Win", "Win/Loss", default=True, enable_events=True, key="Win", size=(20, 10), font=("Helvetica", 20)),
               sg.Radio("Tank", "Role", default=True, enable_events=True, key="Tank", size=(20, 10), font=("Helvetica", 20))],
                                            # row 3
              [sg.Radio("Loss", "Win/Loss", default=False, enable_events=True, key="Loss", size=(20, 10), font=("Helvetica", 20)),
               sg.Radio("DPS", "Role", default=False, enable_events=True, key="DPS", size=(20, 10), font=("Helvetica", 20))],
                                            # row 4
              [sg.Radio("Support", "Role", default=False, enable_events=True, key="Support", size=(20, 10), font=("Helvetica", 20), pad=(368, 0))],
                                            # row 5
              [sg.Button("Cancel", size=(20, 10), font=("Helvetica", 20)), sg.Button("Submit", size=(20, 10), font=("Helvetica", 20))]]


    InputWindow = sg.Window('Overwatch Stats Program', layout, margins=(100, 100))

    while True:  # while the window is active do this
        event, values = InputWindow.read()
        if (event == 'Cancel' or event == sg.WIN_CLOSED):
            InputWindow.close()
            print("cancelled add game, nothing was added")
            sys.exit(0)

        if (event == 'Win'):
            print("win")
            # mydata.at[0, 'totalWon'] += 1   # just... no
            gameOutcome = "win"
        if (event == 'Loss'):
            print("loss")
            # mydata.at[0, 'totalLost'] += 1  # please stop
            gameOutcome = "loss"

        if (event == 'Tank'):
            print("Tank")
            role = "Tank"
        if (event == 'DPS'):
            print("DPS")
            role = "DPS"
        if (event == 'Support'):
            print("Support")
            role = "Support"

        if (event == 'Submit'):
            print("submitted")
            break
    # closes the window after the loop breaks
    InputWindow.close()
    # print(addrow(gameOutcome, role, givendata))
    return addrow(gameOutcome, role, givendata)


''' READING IN THE EXCEL FILE '''

# reading in the file to a pandas dataframe
mydata = pd.read_excel("OverwatchRankStats.xlsx")

# if these columns do not exist add them
if ('Win/Loss/Draw' not in mydata.columns):
    mydata['Win/Loss/Draw'] = []
    print("added win/loss/draw")

if ('Role' not in mydata.columns):
    mydata['Role'] = []
    print("added role")

# removes any unwanted columns that may have been created
mydata = mydata[ ['Win/Loss/Draw', 'Role'] ]


''' WELCOME WINDOW '''

layout = [[sg.Text("Welcome to my Overwatch Stats Program", font=("Helvetica", 40))],
          [sg.Button("Exit", size=(20, 10), font=("Helvetica", 20)),
           sg.Button("See Stats", size=(20, 10), font=("Helvetica", 20)),
           sg.Button("Add Game", size=(20, 10), font=("Helvetica, 20"))]]

WelcomeWindow = sg.Window('Overwatch Stats Program', layout, margins=(100, 100))

while True:  # while the window is active do this
    event, values = WelcomeWindow.read()
    if (event == sg.WIN_CLOSED):
        WelcomeWindow.close()
        sys.exit(0)
        break
    if (event == 'Exit'):
        WelcomeWindow.close()
        print("exited")
        #sys.exit(0)
        break
    if (event == 'See Stats'):
        WelcomeWindow.close()
        displayStats(mydata)
        break
    if (event == 'Add Game'):
        WelcomeWindow.close()
        mydata = addGame(mydata)
        break
# closes the window after the loop breaks
WelcomeWindow.close()

# applying the dataframe changes to the file
print(mydata)
mydata.to_excel("OverwatchRankStats.xlsx")
sys.exit(0)



















