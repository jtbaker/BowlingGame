import requests
import json, jsonpickle

def getplayerslist():
    playerslist = input("Please input your space separated names. ").split()
    requests.post(url='http://localhost:5000/bowlingapi/gamedetails', json={'players':playerslist})
    return playerslist

playerslist = getplayerslist()

for framenumber in range(10):
    for name in playerslist:
        frame = input("Please enter your space separated number of pins knocked down. ")
        scoreboard = requests.post(url=f'http://localhost:5000/bowlingapi/frameinput/{name}', json={'pinsdown':frame})
        print(json.dumps(scoreboard.json()[name],indent=2))
