#!flask/bin/python3.6

from flask import Flask, abort, jsonify, make_response, request, render_template, redirect, url_for
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

# The object that represents the game details for each individual player. Initiates the variables name,
# frames, framescore, runningtotal, which we will subsequently operate on.
class Game:
    def __init__(self, name):
        self.name = name
        self.frames = []
        self.framescore = []
        self.runningtotal = []
        self.gameinprogress = True

    def update(self, pinsdown):
        self.frames.append(pinsdown)

    def recursion(self):
        # Recursions for updating 'framescore' based on new frames. Evaluates before new frames are scored.

        # Two consecutive strikes.
        try:
            if 'X' in self.frames[-3] and len(self.frames[-2]) == 1 and self.framescore[-1:] != self.framescore[9:]:
                self.framescore[-2] += sum(value_index[a] for a in self.frames[-1][:1])
        except IndexError:
            pass

        if self.framescore[-1:] == self.framescore[9:]:
            if 'X' in self.frames[-2:-1] and 'X' in self.frames[-1][0]:
                self.framescore[-2] += sum(value_index[a] for a in self.frames[-1][1:2])

        # One consecutive strike
        try:
            if 'X' in self.frames[-2]:
                self.framescore[-1] += sum(value_index[a] for a in scorecase(self.frames[-1][0:2]))
        except IndexError:
            pass

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
        elif '/' in self.frames[-1]:
            self.framescore.append(value_index['/'])

        # Anything else
        else:
            self.framescore.append(sum([value_index[a] for a in scorecase(self.frames[-1])]))

        # Updating the previous running total if new bowls have changed the values.
        if framenumber == 1 and self.runningtotal[-1] != sum(self.framescore):
            self.runningtotal[-1] = sum(self.framescore[:-1])
        if framenumber >= 2 and self.runningtotal[-2] != sum(self.framescore[:-1]):
            self.runningtotal[-2] = sum(self.framescore[:-2])

        # Appending the new running total to each new instance of a frame. The sum of the current scores for all players.
        self.runningtotal += [sum(self.framescore)]

    # Evaluates on the final frame in the range, if that frame was a strike or a spare.
    def finalframe(self, pinsdown, name):
        if 'X' in self.frames[-1][:1]:
            self.frames[-1].extend(pinsdown)
            self.framescore[-1] = sum([value_index[a] for a in [scorecase(a) for a in (self.frames[-1][0:3])]])
            self.runningtotal[-1] = sum(self.framescore)
            if 'X' in self.frames[-2]:
                self.framescore[-2] =  value_index[scorecase(self.frames[-2][0])] + sum([value_index[a] for a in [scorecase(a) for a in (self.frames[-1][0:2])]])
            if bool(self.frames[-1][2:3]) is True:
                self.gameresults = f'Game over, {name}. Final score: {self.runningtotal[-1]}'
                self.gameinprogress = False
        elif '/' in self.frames[-1][1:2]:
            self.frames[-1].extend(pinsdown[:1])
            self.framescore[-1] = sum([value_index[scorecase(self.frames[-1][1])], value_index[scorecase(self.frames[-1][2])]])
            self.runningtotal[-1] = sum(self.framescore)
            self.gameresults = f'Game over, {name}. Final score: {self.runningtotal[-1]}'
            self.gameinprogress = False
        else:
            self.gameresults = f'Game over, {name}. Final score: {self.runningtotal[-1]}'
            self.gameinprogress = False
        return jsonpickle.encode(gameframe)


# This function evaluates the items in a given frame. An iterable is passed into the function, which checks to see if
# a spare is a part of the frame. If so, only that values is returned. If not, all the items in the argument are
# returned from the function.
def scorecase(items):
    if '/' in items:
        return '/'
    else:
        return items


# Getting the player names, and assigning their Game objects as the associated values, into our dictionary.
@app.route('/bowlingapi/gamedetails', methods=['POST'])
def gamedetails():
    gamedetails = request.json.get('players', "")
    gameframe.update({name:Game(name) for name in gamedetails})
    return make_response(jsonpickle.encode(gameframe))


# The game's main endpoint to get the full scorecoard at any time.
@app.route('/bowlingapi/game', methods=['GET'])
def response():
    return jsonpickle.encode(gameframe)


# A scoring function that evaluates the contents of each frame, and scores it based on its contents.
# Takes arguments name (from the 'name' object for each player in the dictionary for reference, which we get from the API endpoint.
# and frame number.
@app.route('/bowlingapi/frameinput/<name>', methods=['POST'])
def frameinput(name):
    pinsdown = request.json.get('pinsdown', "").split()
    pinsdown = [a if a in value_index else 'Error' for a in pinsdown]
    if 'Error' in pinsdown or sum([value_index[a] for a in pinsdown if a.isdigit() is True]) > 9 or bool(pinsdown) is False:
        return make_response(jsonify({name:{"Invalid Input": True, "gameinprogress": True}}))
    print(type(gameframe[name]),gameframe.get(name))
    framenumber = len(gameframe[name].frames)
    if framenumber <= 9:
        gameframe[name].update(pinsdown)
        gameframe[name].recursion()
        gameframe[name].scoring(framenumber)
    if framenumber == 10 and gameframe[name].gameinprogress is True:
        gameframe[name].finalframe(pinsdown, name)
    return jsonpickle.encode(gameframe)

if __name__ == '__main__':
    app.run(debug=True)
    quit()
