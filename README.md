# BowlingGame

This is server side a script that keeps track of the scores of a bowling game. It runs on a virtual machine using Python3.6, with dependencies of the Flask, JSONPickle, and Json Libraries.

To run it, make sure it is configured as an executable file with <code>chmod a+x ./BowlingGame.py</code> from the directory. Then activate the virtual environment using the command <code>source flask/bin/activate</code> Then run the file, using <code>./BowlingGame.py</code>

It takes JSON inputs from a user on a few different REST API endpoints, calcutes the score of each frame, and the total score of the game, and returns the current total of the game to the user. These run on the interpreter configured in the Virtual Machine installed on the flask directory.

The REST endpoints, once the server is initiated and running, are as follows: 

Takes the player names as a list in JSON format, with key 'players'. POST method.<br>'http:localhost:/bowlingapi/gamedetails'

Takes the number of pins down as space separated string input for each frame with JSON key 'pinsdown', for each player in the game. Takes the variable 'name', as entered at the gamedetails endpoint. Returns a JSON serialized representation of the object in the class with the details for the game so far. POST method.<br>'http:localhost:/bowlingapi/frameinput/name'

There is a short client side example script written to use the API as well, utilizing the Requests and JSON library.

Thanks for checking out my project! More to come. Will be incorporating a GUI front end view in the future.
