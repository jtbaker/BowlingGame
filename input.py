#!flask/bin/python3.6

import requests
import json

def getplayerslist():
    playerslist = input("Please input your space separated names. ").split()
    requests.post(url='http://localhost:5000/bowlingapi/gamedetails', json={'players':playerslist})
    return playerslist
playerslist = getplayerslist()

framenumber=1

while framenumber <=12:
    for name in playerslist:
        frame = input("Please enter your space separated number of pins knocked down. ")
        try:
            scoreboard = requests.post(url=f'http://localhost:5000/bowlingapi/frameinput/{name}', json={'pinsdown':frame})
            print(json.dumps(scoreboard.json()[name],indent=2))
            framenumber += 1
        except KeyError:
            continue
