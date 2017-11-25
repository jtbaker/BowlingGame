import requests
from flask import Flask, abort, jsonify, make_response, request
import json

app = Flask(__name__)

r = requests.get('https://api.github.com/user', auth=('user','password'))

# Matrix for evaluating the values of pins down. '/' denotes a spare, and 'X' a strike.
value_index = {
    '0': 0,
    '1': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'X': 10,
    '/': 10
}

# Function to get pin input from the user.
def inputfunction():
    pinsdown=[a if a in value_index else 'Error' for a in input(
        "Please enter the space-separated value(s) for the pins that you knocked down. 0-9 for open/partial frames, '/' for a spare, and 'X' for a strike. ").split()]
    #Testing for invalid input
    while 'Error' in pinsdown or bool(pinsdown) == False or sum([value_index[a] for a in pinsdown if a.isdigit() is True]) > 9:
        pinsdown=[a if a in value_index else 'Error' for a in input(
            "I'm sorry, that was invalid input. Please enter the space-separated value(s) for the pins that you knocked down.\n0-9 for open/partial frames, '/' for a spare, and 'X' for a strike. If digits, the sum should be no greater than 9. ").split()]
    return pinsdown

# This function evaluates the items in a given frame. An iterable is passed into the function, which checks to see if a score or a strike are a part of the frame. If so, only those values are returned. If not, all the items in the argument are returned from the function.
def scorecase(items):
    if 'X' in items:
        return 'X'
    elif '/' in items:
        return '/'
    else:
        return items

# Getting the number of players in the game
def getplayercount():
    playercount = float(input("How many players are in your game today? Please reply with a whole number. "))
    #playercount = requests.get(url="https://bowlinggame.com", params="How many players are in your game today? Please reply with a whole number")
    # Accounting for nonvalid input in the getplayercount function
    if playercount != abs(int(playercount)):
        while playercount != abs(int(playercount)):
            playercount = float(input(" I'm sorry, that was not a valid answer. How many players are in your game today? Please reply with a whole number. "))
            #playercount = requests.get(url="https://bowlinggame.com", params="I'm sorry, that was invalid input. Please try again. Whole numbers only. ")
    return int(playercount)

# Getting each player's name in the game.
def getname():
    playername = input("Please enter your name. ")
    #playername = requests.get(url="https://bowlinggame.com",
                               #params="Please enter your name.")
    return str(playername)

# A scoring function that evaluates the contents of each frame, and scores it based on its contents.
# Takes arguments name (from the getname() object for each player in the dictionary for reference,
# and framenumber (the frame number (minus one, since we are starting from zero in our iteration).
def scoring(name, framenumber):
    # Local variable for quick reference
    entry = gameframe.get(name)

    # Getting the frame details into a list.
    pinsdown = inputfunction()

    #Attaching the frame details to my dictionary.
    entry['frames'].append(pinsdown)
    entry['framescontinuous'].extend(pinsdown)

    # Recursions for updating 'framescore' based on new frames. Evaluates before new frames are scored.

    # Two consecutive strikes.
    if 'X' in entry['framescontinuous'][-3:-2] and len(entry['frames'][-2]) == 1:
        print("\n\n\n",gameframe,'\n\n\n')
        if ['X','X'] == entry['framescontinuous'][-4:-2]:
            # Max value for a strike is 30 points. Testing to invalidate invalid recursions for consecutive strikes.
            if entry['framescore'][-2] <= 20:
                entry['framescore'][-2] += sum([value_index[a] for a in scorecase(entry['frames'][-1][0])])
            else:
                pass
            if entry['framescore'][-1] <= 20:
                entry['framescore'][-1] += sum([value_index[a] for a in scorecase(entry['framescontinuous'][-2:])])
            else:
                pass
        else:
            try:
                entry['framescore'][-2] += value_index[scorecase(entry['framescontinuous'][-1])]
            except IndexError:
                entry['framescore'][-1] += value_index[scorecase(entry['framescontinuous'][-1])]

    # One consecutive strike
    if 'X' in entry['framescontinuous'][-2:-1]:
        if '/' in entry['frames'][-1]:
            entry['framescore'].append(value_index['/'])
        else:
            if len(entry['frames'][-1]) > 1:
                entry['framescore'][-1] += sum([value_index[a] for a in scorecase(entry['framescontinuous'][-2:])])
            elif len(entry['frames'][-1]) <= 1:
                entry['framescore'][-1] += sum([value_index[a] for a in scorecase(entry['framescontinuous'][-1:])])

    # Spare recursions.
    try:
        if '/' in entry['frames'][-2]:
            entry['framescore'][-1] += value_index[entry['frames'][-1][0]]
    except IndexError:
        pass

    # Scoring section.

    # Scoring a strike in any given frame.
    if 'X' in entry['frames'][-1]:
        entry['framescore'].append(value_index['X'])

    # Scoring spares
    elif '/' in entry['framescontinuous'][-1:]:
        entry['framescore'].append(value_index['/'])

    # Anything else
    else:
        entry['framescore'] += [sum([value_index[scorecase(a)] for a in scorecase(entry['framescontinuous'][-2:])])]

    # Updating the previous running total if new bowls have changed the values.
    if framenumber >= 1 and entry['runningtotal'] != sum(entry['framescore']):
        entry['runningtotal'][-1] = sum(entry['framescore'][:-1])

    # Appending the new running total to each new instance of a frame. The sum of the current scores for all players.
    entry['runningtotal'] += [sum(entry['framescore'])]

    # Final frame - only evaluates if a strike or spare is bowled.
    if framenumber == 9 and entry['framescontinuous'][-1] in ('X','/'):
        print("This is the last frame. To determine the value of your last roll, please bowl again")
        pinsdown = inputfunction()
        entry['frames'][-1].extend(pinsdown)
        entry['framescontinuous'].extend(pinsdown)
        if '/' in entry['framescontinuous'][-1]:
            print("Line 114 is hitting")
            entry['framescore'][-1] += value_index['/']
            print("YESS!!!!")
        else:
            entry['framescore'][-1] += value_index[scorecase(pinsdown[0])]
        entry['runningtotal'][-1] = sum(entry['framescore'])
        # If a second strike is bowled on the final frame.
        if entry['framescontinuous'][-1] == 'X':
            pinsdown = inputfunction()
            entry['frames'][-1].extend(pinsdown)
            entry['framescontinuous'].extend(pinsdown)
            entry['framescore'][-1] += value_index[scorecase(pinsdown[0])]
            entry['runningtotal'][-1] = sum(entry['framescore'])

# Assigning the function call to a variable.
playercount = getplayercount()

# A new, empty frame dictionary object with the details for each player in the game.
gameframe = {getname(): {'frames':[], 'framescontinuous':[], 'framescore':[], 'runningtotal':[]} for player in range(playercount)}

for framenumber in range(10):
    for player in gameframe:
        # Getting the frame details into a list.
        scoring(player,framenumber)
    # Uncomment the line below to view the contents of each section as the recursion evaluates.
    # print(json.dumps(gameframe, indent=2))

