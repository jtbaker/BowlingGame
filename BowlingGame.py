#!flask/bin/python3.6

from flask import Flask, abort, jsonify, make_response, request, render_template
import jsonpickle, json

app = Flask(__name__)

# Dictionary object the represents the individual game/scoring for each player.
# Each Player's name key will have a Game object associated as the value.
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

# The object that represents the game details for each individual player. Initiates the variables name, framescontinuous,
# frames, framescore, runningtotal, which we will subsequently operate on.
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

    def recursion(self):
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
                self.framescore[-1]+=(value_index['/'])
            else:
                if len(self.frames[-1]) > 1:
                    self.framescore[-1]+=sum([value_index[a] for a in scorecase(self.framescontinuous[-2:])])
                elif len(self.frames[-1]) <= 1:
                    self.framescore[-1]+=sum([value_index[a] for a in scorecase(self.framescontinuous[-1:])])

        # Spare recursions.
        try:
            if '/' in self.frames[-2]:
                self.framescore[-1] += value_index[self.frames[-1][0]]
        except IndexError:
            pass

    def scoring(self, framenumber):
        # Scoring a strike in any given frame.
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
    def finalframe(self, framenumber, pinsdown, name):
        if framenumber == 10 and self.framescontinuous[-1] in ('X', '/'):
            self.frames[-1].extend(pinsdown)
            self.framescontinuous.extend(pinsdown)
            self.recursion()
            if len(self.frames[-1]) <=2:
                if '/' in self.frames[-1]:
                    self.framescore[-1] += value_index[scorecase(pinsdown[-1][0])]
                else:
                    self.framescore[-1]+=value_index[scorecase(self.framescontinuous[-2:])]
            self.runningtotal[-1]=sum(self.framescore)
            # If a second strike is bowled on the final frame.
            # if self.framescontinuous[-1] == 'X':
            #     # pinsdown=inputfunction()
            #     self.frames[-1].extend(pinsdown)
            #     self.framescontinuous.extend(pinsdown)
            #     self.framescore[-1]+=value_index[scorecase(pinsdown[0])]
            #     self.runningtotal[-1]=sum(self.framescore)
        return jsonpickle.encode(gameframe)


# This function evaluates the items in a given frame. An iterable is passed into the function, which checks to see if a score or a strike are a part of the frame. If so, only those values are returned. If not, all the items in the argument are returned from the function.
def scorecase(items):
    if 'X' in items:
        return 'X'
    elif '/' in items:
        return '/'
    else:
        return items

# Getting the player names, and assigning their Game objects as the associated values, into our dictionary.
@app.route('/bowlingapi/gamedetails', methods=['POST'])
def gamedetails():
    gamedetails = request.json.get('players', "")
    gameframe.update({name:Game(name) for name in gamedetails})
    return jsonpickle.encode(gameframe)


# A scoring function that evaluates the contents of each frame, and scores it based on its contents.
# Takes arguments name (from the 'name' object for each player in the dictionary for reference, which we get from the API endpoint.
# and frame number.
@app.route('/bowlingapi/frameinput/<name>', methods=['POST'])
def frameinput(name):
    pinsdown = request.json.get('pinsdown', "").split()
    pinsdown = [a if a in value_index else 'Error' for a in pinsdown]
    if 'Error' in pinsdown or sum([value_index[a] for a in pinsdown if a.isdigit() is True]) > 9:
        return make_response(jsonify({name: 'Invalid Input'}))
    else:
        framenumber = len(gameframe[name].frames)
        if framenumber <= 9:
            gameframe[name].update(pinsdown)
            gameframe[name].recursion()
            gameframe[name].scoring(framenumber)
        if framenumber == 10:
            gameframe[name].finalframe(framenumber, pinsdown, name)
        return jsonpickle.encode(gameframe, keys=True)

if __name__ == '__main__':
    app.run(debug=True)
