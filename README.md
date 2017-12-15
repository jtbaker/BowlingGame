# Bowling Game

<h4>Synopsis</h4>
This is a server side application that keeps track of the scores of a bowling game. It runs on a virtual machine using Python3.6 with the <code>flask</code> framework, with dependencies of the <code>jsonpickle</code>, and <code>json</code> Libraries.

It takes JSON inputs from a user on a few different REST API endpoints, calcutes the score of each frame, and the total score of the game, and returns the current game information to the user. These run on the interpreter configured in the Virtual Machine installed on the flask directory.

<h4>Setup Instructions</h4>
To run it, make sure it is configured as an executable file with <code>$ chmod a+x ./BowlingGame.py</code> from the directory. Then activate the virtual environment using the command <code>$ source flask/bin/activate</code> Then run the file, using <code>$ ./BowlingGame.py</code>

<h4>The REST endpoints, once the server is initiated and running, are as follows:<h4>
<h5>Game details</h5>
Takes the player names as a list in JSON format, with key 'players'. POST method.<br>
<a href=http:localhost:5000/bowlingapi/gamedetails>http:localhost:5000/bowlingapi/gamedetails</a>
<ul>
  <li><p>Example request using CURL: <code>$ curl -i -H "Content-Type: application/json" -X POST -d '{"players":[Mark, Eric, John]}' http://localhost:5000/bowlingapi/gamedetails</code></p></li>
  <li><p>Example request using Python's <code>Requests</code> module:<code>requests.post(url=f'http://localhost:5000/bowlingapi/gamedetails', json={'players':[Mark, Eric, John]})</code></p></li></ul>

<h5>Game Information</h5>
Get information at for the game at anytime. Takes <code>GET</code> requests.
<a href=http:localhost:5000/bowlingapi/game>http:localhost:5000/bowlingapi/game</a>
    <ul>
      <li><p>Example request using CURL: <code>$ curl -i http:localhost:5000/bowlingapi/game</code></p></li>
      <li><p>Example request using Python's <code>Requests</code> module:<code>requests.get(url='http://localhost:5000/bowlingapi/game')</code></p></li>
    </ul>

<h5>Frame Input</h5>
Takes the number of pins down as space separated string input for each frame with JSON key 'pinsdown', for each player in the game. Takes the variable 'name', as entered at the gamedetails endpoint. Returns a JSON serialized representation of the object in the class with the details for the game so far. POST method.<br>
<a href=http:localhost:5000/bowlingapi/frameinput/name>http:localhost:5000/bowlingapi/frameinput/name</a>
<ul>
  <li><p>Example request using CURL: <code>$ curl -i -H "Content-Type: application/json" -X POST -d '{"pinsdown":"4 /"}' http://localhost:5000/bowlingapi/frameinput/name</code><p></li>
  <li><p>Example request using Python's <code>Requests</code> module: <code>requests.post(url=f'http://localhost:5000/bowlingapi/frameinput/Mark', json={'pinsdown':'4 /'})</code></p></li></ul>
  <br>
  
<h4>Client side</h4>
<p>There is a short client side example script written to use the API as well, utilizing the Requests and JSON library.
Thanks for checking out my project! More to come. Will be incorporating a GUI front end view in the future.</p>
