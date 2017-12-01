#!flask/bin/python3.6

from flask import Flask, abort, jsonify, make_response, request, render_template
import jsonpickle, json

app = Flask(__name__)

gameframe = {}

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

class Game:
    def __init__(self, name):
        self.name = name
        self.framescontinuous = []
        self.frames = []
        self.framescore = []
        self.runningtotal = []

    def update(self, pinsdown):
        self.frames.append(pinsdown)
        self.framescontinuous.extend(pinsdown)

    def recursion(self, pinsdown):
        # Recursions for updating 'framescore' based on new frames. Evaluates before new frames are scored.

        # Two consecutive strikes.
        if 'X' in self.framescontinuous[-3:-2] and len(self.frames[-2]) == 1:
            if ['X', 'X'] == self.framescontinuous[-4:-2]:
                # Max value for a strike is 30 points. Testing to invalidate invalid recursions for consecutive strikes.
                if self.framescore[-1] <= 20:
                    self.framescore[-1]+=sum([value_index[a] for a in scorecase(self.framescontinuous[-2:])])
                else:
                    if self.framescore[-2] <= 20:
                        self.framescore[-2]+=sum([value_index[a] for a in scorecase(self.frames[-1][0])])
                if self.framescore[-2] <= 20:
                    self.framescore[-2] += sum([value_index[a] for a in scorecase(self.frames[-1][0])])
            else:
                try:
                    self.framescore[-2]+=value_index[scorecase(self.framescontinuous[-1])]
                except IndexError:
                    self.framescore[-1]+=sum([value_index[a] for a in scorecase(self.framescontinuous[-2:])])

        # One consecutive strike
        if 'X' in self.framescontinuous[-2:-1] and ['X', 'X'] != self.framescontinuous[-4:-2]:
            if '/' in self.frames[-1]:
                self.framescore.append(value_index['/'])
            else:
                if len(self.frames[-1]) > 1:
                    self.framescore[-1]+=sum([value_index[a] for a in scorecase(self.framescontinuous[-2:])])
                elif len(self.frames[-1]) <= 1:
                    self.framescore[-1]+=sum([value_index[a] for a in scorecase(self.framescontinuous[-1:])])

        # Spare recursions.
        try:
            if '/' in self.frames[-2]:
                self.framescore[-1]+=value_index[self.frames[-1][0]]
        except IndexError:
            pass

    # Scoring a strike in any given frame.
    def scoring(self, framenumber):
        if 'X' in self.frames[-1]:
            self.framescore.append(value_index['X'])

        # Scoring spares
        elif '/' in self.framescontinuous[-1:]:
            self.framescore.append(value_index['/'])

        # Anything else
        else:
            self.framescore += [sum([value_index[scorecase(a)] for a in scorecase(self.framescontinuous[-2:])])]

        # # Updating the previous running total if new bowls have changed the values.
        if framenumber >= 1 and self.runningtotal[-1] != sum(self.framescore):
            self.runningtotal[-1] = sum(self.framescore[:-1])
        if framenumber >= 2 and self.runningtotal[-2] != sum(self.framescore[:-1]):
            self.runningtotal[-2] = sum(self.framescore[:-2])

        # Appending the new running total to each new instance of a frame. The sum of the current scores for all players.
        self.runningtotal += [sum(self.framescore)]

    # Evaluates on the final frame in the range, if that frame was a strike or a spare.
    def finalframe(self, framenumber, pinsdown):
        if framenumber == 10 and self.framescontinuous[-1] in ('X', '/'):
            print("This is the last frame. To determine the value of your last roll, please bowl again")
            self.frames[-1].extend(pinsdown)
            self.framescontinuous.extend(pinsdown)
            if '/' in self.framescontinuous[-1]:
                self.framescore[-1]+=value_index['/']
            else:
                self.framescore[-1]+=value_index[scorecase(pinsdown[0])]
            self.runningtotal[-1]=sum(self.framescore)
            # If a second strike is bowled on the final frame.
            # if self.framescontinuous[-1] == 'X':
            #     # pinsdown=inputfunction()
            #     self.frames[-1].extend(pinsdown)
            #     self.framescontinuous.extend(pinsdown)
            #     self.framescore[-1]+=value_index[scorecase(pinsdown[0])]
            #     self.runningtotal[-1]=sum(self.framescore)
        return jsonpickle.encode(gameframe)

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
@app.route('/bowlingapi/<int:playercount>', methods=['POST'])
def getplayercount(playercount):
    # playercount = float(input("How many players are in your game today? Please reply with a whole number. "))
    #playercount = requests.get(url="https://bowlinggame.com", params="How many players are in your game today? Please reply with a whole number")
    # Accounting for nonvalid input in the getplayercount function
    if playercount != abs(int(playercount)):
        return int(playercount)

# playercount = getplayercount(playercount)
#         # while playercount != abs(int(playercount)):
#         #     playercount = float(input(" I'm sorry, that was not a valid answer. How many players are in your game today? Please reply with a whole number. "))
#             #playercount = requests.get(url="https://bowlinggame.com", params="I'm sorry, that was invalid input. Please try again. Whole numbers only. ")


@app.route('/bowlingapi/gamedetails', methods=['POST'])
def gamedetails():
    gamedetails = request.json.get('players', "")
    gameframe.update({name:Game(name) for name in gamedetails})
    return jsonpickle.encode(gameframe)

# Getting each player's name in the game.
@app.route('/bowlingapi/names/<playername>', methods=['POST'])
def getname():
    playername = input("Please enter your name. ")
    return playername
    #playername = requests.get(url="https://bowlinggame.com",
                               #params="Please enter your name.")

# A scoring function that evaluates the contents of each frame, and scores it based on its contents.
# Takes arguments name (from the 'name' object for each player in the dictionary for reference,
# and framenumber (the frame number (minus one, since we are starting from zero in our iteration).
# @app.route('/Bowlingapi/scoring/<str:pinsdown>', methods=['PUT'])
@app.route('/bowlingapi/frameinput/<name>', methods=['POST'])
def frameinput(name):
    pinsdown = request.json.get('pinsdown', "").split()
    framenumber = len(gameframe[name].frames)
    if framenumber <= 9:
        gameframe[name].update(pinsdown)
        gameframe[name].recursion(pinsdown)
        gameframe[name].scoring(framenumber)
    if framenumber == 10:
        gameframe[name].finalframe(framenumber, pinsdown)
    # if framenumber == 10:
    #     return abort(200)
    # framenumber = len(gameframe[name].frames)
    # except IndexError:
    #     return make_response(jsonify({'error': 'Not found'}))
    # gameframe['Jason'].update(pinsdown)
    # gameframe['Jason'].recursion(pinsdown)
    # framenumber = len(gameframe['Jason']['frames'])
    return jsonpickle.encode(gameframe, keys=True)
# Assigning the function call to a variable.
# playercount = getplayercount()
# Getting the names for the players.
# names=[getname() for player in range(playercount)]
# A new, empty frame dictionary object with the details for each player in the game.

# def playbowling():
#     for framenumber in range(10):
#         for player in gameframe:
#             # Getting the frame details into a list.
#             scoring(gameframe[player],framenumber)
#         # Uncomment the line below to view the contents of each section as the iteration evaluates.
#         print(jsonpickle.encode(gameframe))

if __name__ == '__main__':
    app.run(debug=True)