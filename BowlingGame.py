import requests
import json

r = requests.get('https://api.github.com/user', auth=('user','password'))

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

def scorecase(items):
    if 'X' in items:
        return 'X'
    elif '/' in items:
        return '/'
    else:
        return items

#Getting the number of players in the game
def getplayercount():
    playercount = float(input("How many players are in your game today? Please reply with a whole number. "))
    #playercount = requests.get(url="https://bowlinggame.com", params="How many players are in your game today? Please reply with a whole number")
    # Accounting for nonvalid input in the getplayercount function
    if playercount != abs(int(playercount)):
        while playercount != abs(int(playercount)):
            playercount = float(input("How many players are in your game today? Please reply with a whole number. "))
            #playercount = requests.get(url="https://bowlinggame.com", params="I'm sorry, that was invalid input. Please try again. Whole numbers only. ")
    return int(playercount)

def getname():
    playername = input("Please enter your name. ")
    #playername = requests.get(url="https://bowlinggame.com",
                               #params="Please enter your name.")
    return str(playername)

# def strikescores(iterable):
#     if '/' or 'X' in iterable:
#         return value_index
#     if

def scoring(name):
    #local variable for quick reference
    entry = gameframe.get(name)

    #Getting the frame details into a list.
    pinsdown = inputfunction()
    #Attaching the frame details to my dictionary.
    entry['frames'].append(pinsdown)
    entry['framescontinuous'].extend(pinsdown)

    #Recursion for updating 'framescore' based on new frames.
    # if '-' in entry['framescore'][-1:]:
    #     entry['framescore'][-1] = sum([value_index[scorecase(a[1])] for a in entry['frames'][-3:]])
    #     entry['runningtotal'][-1] = sum(entry['framescore'])
    if 'X' in entry['framescontinuous'][-3:-2] and len(entry['frames'][-2]) == 1:
        print("Line 65 is hitting")
        try:
            entry['framescore'][-2] += value_index[scorecase(entry['framescontinuous'][-1])]
        except IndexError:
            print("Line 69 is hitting")
            entry['framescore'][-1] += value_index[scorecase(entry['framescontinuous'][-1])]

    if 'X' in entry['framescontinuous'][-4:-3] and len(entry['frames'][-2]) == 1:
        print("Line 72 is hitting")
        entry['framescore'][-3] += value_index[scorecase(entry['frames'][-1][0])]

    if 'X' in entry['framescontinuous'][-2:-1]:
        print("Line 76 is hitting")
        if '/' in entry['frames'][-1]:
            entry['framescore'].append(value_index['/'])
            print("YESS!!!!")
        else:
            if len(entry['frames'][-1]) > 1:
                print("Line 82 is hitting")
                entry['framescore'][-1] += sum([value_index[a] for a in scorecase(entry['framescontinuous'][-2:])])
            elif len(entry['frames'][-1]) <= 1:
                print("Line 85 is hitting")
                entry['framescore'][-1] += sum([value_index[a] for a in scorecase(entry['framescontinuous'][-1:])])

    # if 'X' in entry['framescontinuous'][-2:-1] and len(entry['frames'][-2]) <= 1:
    #     entry['framescore'][-1] += value_index[scorecase(entry['framescontinuous'][-1])]
    #
    # else:
    # if 'X' in entry['framescontinuous'][-3:-2] and len(entry['frames'][-2]) <= 1:
    #     entry['framescore'][-1] += value_index[scorecase(entry['framescontinuous'][-1])]

    if '/' in entry['frames'][-2]:
        print("Line 96 is hitting")
        entry['framescore'][-1] += value_index[entry['frames'][-1][0]]

    entry['runningtotal'] += [sum(entry['framescore'])]

    # Scoring strikes
    # Double Strikes
    # elif 'X' in entry['frames'][-2]:
    #     print('X is here')
    #     entry['framescore'].append(value_index['X'])
    # Single Strikes
    if 'X' in entry['frames'][-1]:
        print("Line 108 is hitting")
        print('X is here')
        entry['framescore'].append(value_index['X'])

    # Scoring spares
    elif '/' in entry['framescontinuous'][-1:]:
        print("Line 114 is hitting")
        entry['framescore'].append(value_index['/'])
        print("YESS!!!!")

    #Everything else
    else:
        print("Line 120 is hitting")
        entry['framescore'] += [sum([value_index[scorecase(a)] for a in scorecase(entry['framescontinuous'][-2:])])]

def inputfunction():
    pinsdown=[a if a in value_index else 'Error' for a in input(
        "Please enter the space-separated value(s) for the pins that you knocked down. 0-9 for open/partial frames, '/' for a spare, and 'X' for a strike. ").split()]
    #Testing for invalid input
    while 'Error' in pinsdown or bool(pinsdown) == False or sum([value_index[a] for a in pinsdown if a.isdigit() is True]) > 9:
        pinsdown=[a if a in value_index else 'Error' for a in input(
            "I'm sorry, that was invalid input. Please enter the space-separated value(s) for the pins that you knocked down.\n0-9 for open/partial frames, '/' for a spare, and 'X' for a strike. If digits, the sum should be no greater than 9. ").split()]
    return pinsdown



playercount = getplayercount()

gameframe = {getname():{'frames':[],'framescontinuous':[],'framescore':[], 'runningtotal':[]} for player in range(playercount)}

# this accounts for the first frame in the game, before the scoring frames.
for playerfirstround in gameframe:
    # Getting the frame details into a list.
    pinsdown = inputfunction()
    # Attaching the frame details to my dictionary.
    gameframe[playerfirstround]['frames'].extend([pinsdown])
    gameframe[playerfirstround]['framescontinuous'].extend(pinsdown)
    if '/' or 'X' not in pinsdown:
        gameframe[playerfirstround]['framescore'].append(sum(value_index[a] for a in pinsdown))
    else:
        continue

print(gameframe)


for framenumber in range(10):
    for player in gameframe:
        # Getting the frame details into a list.
        scoring(player)
        print(gameframe[player])
