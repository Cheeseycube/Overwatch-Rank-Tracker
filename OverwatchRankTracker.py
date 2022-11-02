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

def updateRank(rank, role, givenData):
    if (role == 'Tank'):
        givenData.at[0, 'Rank'] = rank
    if (role == 'DPS'):
        givenData.at[1, 'Rank'] = rank
    if (role == 'Support'):
        givenData.at[2, 'Rank'] = rank
    return givenData

def addrow(gameOutcome, role, givenData):
    try:
        #givendata.loc[len(givendata.index)] = [gameOutcome, role]
        newRow = {"Win/Loss/Draw": gameOutcome, "Role": role}
        if (gameOutcome == "loss"):
            if (role == 'Tank'):
                givenData.at[0, 'Rank'] = givenData.at[0, 'Rank'] - 25
                #newRow = {"Win/Loss/Draw": gameOutcome, "Role": role, "Rank":givenData.at[0, 'Rank']}
            if (role == 'DPS'):
                givenData.at[1, 'Rank'] = givenData.at[1, 'Rank'] - 25
                #newRow = {"Win/Loss/Draw": gameOutcome, "Role": role, "Rank": givenData.at[1, 'Rank']}
            if (role == 'Support'):
                givenData.at[2, 'Rank'] = givenData.at[2, 'Rank'] - 25
                #newRow = {"Win/Loss/Draw": gameOutcome, "Role": role, "Rank": givenData.at[2, 'Rank']}
        if (gameOutcome == "win"):
            if (role == 'Tank'):
                givenData.at[0, 'Rank'] = givenData.at[0, 'Rank'] + 25
                #newRow = {"Win/Loss/Draw": gameOutcome, "Role": role, "Rank": givenData.at[0, 'Rank']}
            if (role == 'DPS'):
                givenData.at[1, 'Rank'] = givenData.at[1, 'Rank'] + 25
                #newRow = {"Win/Loss/Draw": gameOutcome, "Role": role, "Rank": givenData.at[1, 'Rank']}
            if (role == 'Support'):
                givenData.at[2, 'Rank'] = givenData.at[2, 'Rank'] + 25
                #newRow = {"Win/Loss/Draw": gameOutcome, "Role": role, "Rank": givenData.at[2, 'Rank']}
        return givenData.append(newRow, ignore_index=True)
    except:
        print("cannot set a row with mismatched columns OR some other error idk")


def createTankdata(EncodedData):
    Tankdata = EncodedData
    for i in EncodedData.index:
        if (EncodedData["Role"][i] != "Tank"):
            Tankdata = Tankdata.drop([EncodedData.index[i]])
    return Tankdata

def createDPSdata(EncodedData):
    DPSdata = EncodedData
    for i in EncodedData.index:
        if (EncodedData["Role"][i] != "DPS"):
            DPSdata = DPSdata.drop([EncodedData.index[i]])
    return DPSdata

def createSupportdata(EncodedData):
    Supportdata = EncodedData
    for i in EncodedData.index:
        if (EncodedData["Role"][i] != "Support"):
            Supportdata = Supportdata.drop([EncodedData.index[i]])
    return Supportdata

def displayStats(givenData):
    # Calculating Statistics
    EncodedData = pd.get_dummies(givenData, columns=["Win/Loss/Draw"], prefix=["Outcome"])
    Tankdata = createTankdata(EncodedData)
    DPSdata = createDPSdata(EncodedData)
    Supportdata = createSupportdata(EncodedData)

    # total wins/losses
    if ('Outcome_win' in EncodedData.columns):
        Wins = EncodedData["Outcome_win"].sum()
    else:
        Wins = 0

    if ('Outcome_loss' in EncodedData.columns):
        Losses = EncodedData["Outcome_loss"].sum()
    else:
        Losses = 0


    # if statements may be unneccessary here
    # Tank stats
    try:
        Tank_Rank = EncodedData.at[0, 'Rank']
    except:
        Tank_Rank = np.nan

    if ('Outcome_win' in Tankdata.columns):
        Tank_Wins = Tankdata["Outcome_win"].sum()
    else:
        Tank_Wins = 0

    if ('Outcome_loss' in Tankdata.columns):
        Tank_Losses = Tankdata["Outcome_loss"].sum()
    else:
        Tank_Losses = 0

    # DPS stats
    try:
        DPS_Rank = EncodedData.at[1, 'Rank']
    except:
        DPS_Rank = np.nan

    if ('Outcome_win' in DPSdata.columns):
        DPS_Wins = DPSdata["Outcome_win"].sum()
    else:
        DPS_Wins = 0

    if ('Outcome_loss' in DPSdata.columns):
        DPS_Losses = DPSdata["Outcome_loss"].sum()
    else:
        DPS_Losses = 0

    # Support stats
    try:
        Support_Rank = EncodedData.at[2, 'Rank']
    except:
        Support_Rank = np.nan
    if ('Outcome_win' in Supportdata.columns):
        Support_Wins = Supportdata["Outcome_win"].sum()
    else:
        Support_Wins = 0

    if ('Outcome_loss' in Supportdata.columns):
        Support_Losses = Supportdata["Outcome_loss"].sum()
    else:
        Support_Losses = 0

    if (len(EncodedData.index) == 0):
        winPercentage = 100
    else:
        #winPercentage = Wins/len(EncodedData.index) * 100
        try:
            winPercentage = Tank_Wins / (Tank_Wins + Tank_Losses) * 100
        except:
            winPercentage = "na"
    # displaying stats
                                        # row 1
    layout = [[sg.Text(f"Total tank wins: {Tank_Wins}", font=("Helvetica", 20)),
               sg.Text(f"Total tank losses: {Tank_Losses}", font=("Helvetica", 20)), sg.Text(f"Overall tank win percentage: {winPercentage}%", font=("Helvetica", 20))],
                                        # row 2
              [sg.Text(f"Estimated Tank Rank: {Tank_Rank}", font=("Helvetica", 20))],
                                        # row 3
              [sg.Text(f"Estimated DPS Rank: {DPS_Rank}", font=("Helvetica", 20))],
                                        # row 4
              [sg.Text(f"Estimated Support Rank: {Support_Rank}", font=("Helvetica", 20))],
              [sg.Button('Back', size=(5, 2), font=("Helvetica", 20)), sg.Button('Exit', size=(5, 2), font=("Helvetica", 20))]]

    statsWindow = sg.Window('Stats Window', layout, margins=(100, 100))

    while True:
        event, values = statsWindow.read()
        if (event == sg.WIN_CLOSED or event == 'Back'):
            statsWindow.close()
            #sys.exit(0)
            break
        if (event == 'Exit'):
            statsWindow.close()
            sys.exit(0)
    statsWindow.close()
    return givenData


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
            InputWindow.clos()
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

def setRank(givenData):
    col1 = [ [sg.Radio("Bronze 5", "Rank", default=True, enable_events=True, key="Bronze 5", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Bronze 4", "Rank", default=False, enable_events=True, key="Bronze 4", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Bronze 3", "Rank", default=False, enable_events=True, key="Bronze 3", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Bronze 2", "Rank", default=False, enable_events=True, key="Bronze 2", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Bronze 1", "Rank", default=False, enable_events=True, key="Bronze 1", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Silver 5", "Rank", default=False, enable_events=True, key="Silver 5", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Silver 4", "Rank", default=False, enable_events=True, key="Silver 4", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Silver 3", "Rank", default=False, enable_events=True, key="Silver 3", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Silver 2", "Rank", default=False, enable_events=True, key="Silver 2", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Silver 1", "Rank", default=False, enable_events=True, key="Silver 1", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Gold 5", "Rank", default=False, enable_events=True, key="Gold 5", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Gold 4", "Rank", default=False, enable_events=True, key="Gold 4", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Gold 3", "Rank", default=False, enable_events=True, key="Gold 3", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Gold 2", "Rank", default=False, enable_events=True, key="Gold 2", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Gold 1", "Rank", default=False, enable_events=True, key="Gold 1", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Platinum 5", "Rank", default=False, enable_events=True, key="Platinum 5", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Platinum 4", "Rank", default=False, enable_events=True, key="Platinum 4", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Platinum 3", "Rank", default=False, enable_events=True, key="Platinum 3", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Platinum 2", "Rank", default=False, enable_events=True, key="Platinum 2", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Platinum 1", "Rank", default=False, enable_events=True, key="Platinum 1", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Diamond 5", "Rank", default=False, enable_events=True, key="Diamond 5", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Diamond 4", "Rank", default=False, enable_events=True, key="Diamond 4", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Diamond 3", "Rank", default=False, enable_events=True, key="Diamond 3", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Diamond 2", "Rank", default=False, enable_events=True, key="Diamond 2", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Diamond 1", "Rank", default=False, enable_events=True, key="Diamond 1", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Masters 5", "Rank", default=False, enable_events=True, key="Masters 5", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Masters 4", "Rank", default=False, enable_events=True, key="Masters 4", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Masters 3", "Rank", default=False, enable_events=True, key="Masters 3", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Masters 2", "Rank", default=False, enable_events=True, key="Masters 2", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Masters 1", "Rank", default=False, enable_events=True, key="Masters 1", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Grandmaster 5", "Rank", default=False, enable_events=True, key="Grandmaster 5", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Grandmaster 4", "Rank", default=False, enable_events=True, key="Grandmaster 4", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Grandmaster 3", "Rank", default=False, enable_events=True, key="Grandmaster 3", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Grandmaster 2", "Rank", default=False, enable_events=True, key="Grandmaster 2", size=(10, 5), font=("Helvetica", 20))],
              [sg.Radio("Grandmaster 1", "Rank", default=False, enable_events=True, key="Grandmaster 1", size=(10, 5), font=("Helvetica", 20))]
             ]

    layout = [[sg.Text("What's your rank, bozo", font=("Helvetica", 40), size=(20, 1), justification='center')],
              [sg.Column(col1, element_justification='c', scrollable=True, vertical_scroll_only=True),
               sg.Button("Submit", font=("Helvetica", 20), size=(10, 1)),
               sg.Button("Back", font=("Helvetica", 20), size=(10, 1)),
               sg.Button("Exit", font=("Helvetica", 20), size=(10, 1)),
               sg.Radio("Tank", "Role", default=True, enable_events=True, key="Tank", size=(10, 1),
                        font=("Helvetica", 20)),
               sg.Radio("DPS", "Role", default=False, enable_events=True, key="DPS", size=(10, 1),
                        font=("Helvetica", 20)),
               sg.Radio("Support", "Role", default=False, enable_events=True, key="Support", size=(10, 1),
                        font=("Helvetica", 20))]
             ]

    rank = 300
    role = 'Tank'
    def switch(tier, curRank):
        if tier == "Bronze 5":
            return 200           # upper bound: 300
        if tier == "Bronze 4":
            return 500           # upper bound: 600
        if tier == "Bronze 3":
            return 700           # upper bound: 900
        if tier == "Bronze 2":
            return 1100          # upper bound: 1200
        if tier == "Bronze 1":
            return 1450          # upper bound: 1499
        if tier == "Silver 5":
            return 1550          # upper bound: 1600
        if tier == "Silver 4":
            return 1650          # upper bound: 1700
        if tier == "Silver 3":
            return 1750          # upper bound: 1800
        if tier == "Silver 2":
            return 1850          # upper bound: 1900
        if tier == "Silver 1":
            return 1950          # upper bound: 1999
        if tier == "Gold 5":
            return 2050          # upper bound: 2100
        if tier == "Gold 4":
            return 2150          # upper bound: 2200
        if tier == "Gold 3":
            return 2250          # upper bound: 2300
        if tier == "Gold 2":
            return 2350          # upper bound: 2400
        if tier == "Gold 1":
            return 2450          # upper bound: 2499
        if tier == "Platinum 5":
            return 2550          # upper bound: 2600
        if tier == "Platinum 4":
            return 2650          # upper bound: 2700
        if tier == "Platinum 3":
            return 2750          # upper bound: 2800
        if tier == "Platinum 2":
            return 2850          # upper bound: 2900
        if tier == "Platinum 1":
            return 2950          # upper bound: 2999
        if tier == "Diamond 5":
            return 3050          # upper bound: 3100
        if tier == "Diamond 4":
            return 3150          # upper bound: 3200
        if tier == "Diamond 3":
            return 3250          # upper bound: 3300
        if tier == "Diamond 2":
            return 3350          # upper bound: 3400
        if tier == "Diamond 1":
            return 3450          # upper bound: 3499
        if tier == "Masters 5":
            return 3550          # upper bound: 3600
        if tier == "Masters 4":
            return 3650          # upper bound: 3700
        if tier == "Masters 3":
            return 3750          # upper bound: 3800
        if tier == "Masters 2":
            return 3850          # upper bound: 3900
        if tier == "Masters 1":
            return 3950          # upper bound: 3999
        if tier == "Grandmaster 5":
            return 4050  # upper bound: 4100
        if tier == "Grandmaster 4":
            return 4150  # upper bound: 4200
        if tier == "Grandmaster 3":
            return 4250  # upper bound: 4300
        if tier == "Grandmaster 2":
            return 4350  # upper bound: 4400
        if tier == "Grandmaster 1":
            return 4450  # upper bound: 4500+
        else:
            return curRank

    RankSettingWindow = sg.Window('Overwatch Stats Program', layout, margins=(100, 100), size=(1500, 1000))

    while True:  # while the window is active do this
        event, values = RankSettingWindow.read()
        if (event == sg.WIN_CLOSED or event == 'Back'):
            RankSettingWindow.close()
            # return a version of givenData with rank updated
            return givenData
        if (event == 'Exit'):
            RankSettingWindow.close()
            RankSettingWindow.close()
            sys.exit(0)
        if (event == 'Submit'):
            RankSettingWindow.close()
            return updateRank(rank, role, givenData)
        if (event == 'Tank'):
            role = 'Tank'
        if (event == 'DPS'):
            role = 'DPS'
        if (event == 'Support'):
            role = 'Support'
        rank = switch(event, rank)

    # closes the window after the loop breaks
    RankSettingWindow.close()

def welcomeWindow(givenData):
    layout = [[sg.Text("Pick your poison", font=("Helvetica", 40), size=(43, 1), justification='center')],
                [sg.Button("Exit", size=(20, 10), font=("Helvetica", 20)),
                sg.Button("See Stats", size=(20, 10), font=("Helvetica", 20)),
                sg.Button("Add Game", size=(20, 10), font=("Helvetica, 20")),
                sg.Button("Set Rank", size=(20, 10), font=("Helvetica, 20"))]]

    WelcomeWindow = sg.Window('Overwatch Stats Program', layout, margins=(100, 100))

    while True:  # while the window is active do this
        event, values = WelcomeWindow.read()
        if (event == sg.WIN_CLOSED):
            WelcomeWindow.close()
            sys.exit(0)
        if (event == 'Exit'):
            WelcomeWindow.close()
            print("exited")
            sys.exit(0)
        if (event == 'See Stats'):
            WelcomeWindow.close()
            return displayStats(givenData), True
        if (event == 'Add Game'):
            WelcomeWindow.close()
            return addGame(givenData), True
        if (event == 'Set Rank'):
            WelcomeWindow.close()
            return setRank(givenData), True
    # closes the window after the loop breaks
    WelcomeWindow.close()

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

if ('Rank' not in mydata.columns):
    mydata['Rank'] = []
    print("added rank")
# removes any unwanted columns that may have been created
mydata = mydata[ ['Win/Loss/Draw', 'Role', 'Rank'] ]


''' MAIN '''
toWelcomeWindow = True
# infinite loop
while (True):
    if (toWelcomeWindow):
        mydata, toWelcomeWindow = welcomeWindow(mydata)
        mydata.to_excel("OverwatchRankStats.xlsx")
# could have a bool called welcomeWindow that when it is true we open up the welcomeWindow


# applying the dataframe changes to the file
print(mydata)
mydata.to_excel("OverwatchRankStats.xlsx")
sys.exit(0)



















