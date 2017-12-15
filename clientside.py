#!flask/bin/python3.6

import requests
import json


def getplayerslist():
    playerslist = input("Please input your space separated names. ").split()
    requests.post(url='http://localhost:5000/bowlingapi/gamedetails', json={'players':playerslist})
    return playerslist
playerslist = getplayerslist()

scoreboard = requests.get('http://localhost:5000/bowlingapi/game').json()

for name in playerslist:
    while scoreboard[name]['gameinprogress'] is True:
        frame = input("Please enter your space separated number of pins knocked down. ")
        scoreboard = requests.post(url=f'http://localhost:5000/bowlingapi/frameinput/{name}', json={'pinsdown': frame})
        scoreboard = scoreboard.json()
        print(json.dumps(scoreboard,indent=2))
