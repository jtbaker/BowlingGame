# BowlingGame

This is server side a script that keeps track of the scores of a bowling game. It runs on a virtual machine using Python3.6, with dependencies of the <code>flask</code>, <code>jsonpickle</code>, and <code>json</code> Libraries.

To run it, make sure it is configured as an executable file with <code>chmod a+x ./BowlingGame.py</code> from the directory. Then activate the virtual environment using the command <code>source flask/bin/activate</code> Then run the file, using <code>./BowlingGame.py</code>

It takes JSON inputs from a user on a few different REST API endpoints, calcutes the score of each frame, and the total score of the game, and returns the current total of the game to the user. These run on the interpreter configured in the Virtual Machine installed on the flask directory.

The REST endpoints, once the server is initiated and running, are as follows: 
<h4>Game details</h4>
Takes the player names as a list in JSON format, with key 'players'. POST method.<br>
'http:localhost:5000/bowlingapi/gamedetails'
<ul>
  <li><p>Example request using CURL: <code>$ curl -i -H "Content-Type: application/json" -X POST -d '{"players":[Mark, Eric, John]}' http://localhost:5000/bowlingapi/gamedetails</code></p></li>
  <li><p>Example request using Python's <code>Requests</code> module.:<code>requests.post(url=f'http://localhost:5000/bowlingapi/frameinput/Mark', json={'players':[Mark, Eric, John]})</code></p></li></ul>

<h4>Pinsdown</h4>
Takes the number of pins down as space separated string input for each frame with JSON key 'pinsdown', for each player in the game. Takes the variable 'name', as entered at the gamedetails endpoint. Returns a JSON serialized representation of the object in the class with the details for the game so far. POST method.<br>'http:localhost:5000/bowlingapi/frameinput/name'
<ul>
  <li><p>Example request using CURL: <code>$ curl -i -H "Content-Type: application/json" -X POST -d '{"pinsdown":"4 /"}' http://localhost:5000/bowlingapi/frameinput/name</code><p></li>
  <li><p>Example request using Python's <code>Requests</code> module: <code>requests.post(url=f'http://localhost:5000/bowlingapi/frameinput/Mark', json={'pinsdown':'4 /'})</code></p></li></ul>

There is a short client side example script written to use the API as well, utilizing the Requests and JSON library.

Thanks for checking out my project! More to come. Will be incorporating a GUI front end view in the future.
