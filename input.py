import requests
import json

a=requests.post(url='http://localhost:5000/bowlingapi/gamedetails', json={'players':["Jason"]})
print(a.json())

b=requests.post(url='http://localhost:5000/bowlingapi/scoring', json={'pinsdown':["4,5"]})
print(json.dumps(b.json(),indent=2))

c=requests.post(url='http://localhost:5000/bowlingapi/scoring', json={'pinsdown':["6,/"]})
print(json.dumps(c.json(),indent=2))