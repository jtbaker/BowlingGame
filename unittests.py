from unittest import TestCase
import unittest
import requests
import json


# Sample input with frame input, and final scores.
frame_input_samples = {
    "Jason": {"input":['X','X','X','X','X','X','X','X','X','X','X','X'],"score": 300},
    "Mark": {"input":['X','7 /','X','6 /','X','8 /','X','7 /','8','8'],"score": 174},
    "Eric": {"input":['X','7 /','9 0','X','0 8','8 /','0 6','X','X','X','8','1'],"score": 167},
    "Alex": {"input":['9 /','6 3','X','8 /','6 3','X','X','X','8 /','9 /','5'],"score": 182},
}

invalid_input_response={name: {"Invalid Input": True, "gameinprogress": True} for name in frame_input_samples}

valid_response={name:{'py/object':"__main__.Game","frames":[],"framescore":[],"gameinprogress":True, "name":name, "runningtotal":[]} for name in frame_input_samples}


class TestFlaskApiUsingRequests(TestCase):
    # Tests that POSTing an iterable of names returns a valid response.
    def test_add_names(self):
        requests.post('http://localhost:5000/bowlingapi/gamedetails', json={"players": frame_input_samples})
        initialgame = requests.get('http://localhost:5000/bowlingapi/game')
        self.assertEqual(initialgame.json(), valid_response)

    # Tests that invalid input returns a proper error code.
    def test_invalid_input(self):
        response = requests.post('http://localhost:5000/bowlingapi/frameinput/Jason', json={'pinsdown':"F G"})
        self.assertEqual(response.json().get("Jason").get("Invalid Input"),invalid_input_response['Jason'].get("Invalid Input"))

    # Tests that adding a series of framescores returns the proper final score.
    def test_add_frame_score(self):
        requests.post('http://localhost:5000/bowlingapi/gamedetails', json={"players": frame_input_samples})
        for name in frame_input_samples:
            for x in frame_input_samples[name].get('input'):
                requests.post(f'http://localhost:5000/bowlingapi/frameinput/{name}', json={"pinsdown": x})
        response = requests.get('http://localhost:5000/bowlingapi/game')
        self.assertEqual([response.json()[name]['runningtotal'][-1] for name in frame_input_samples], [frame_input_samples[name]["score"] for name in frame_input_samples])
        # To see the result of the final object.
        print(json.dumps(response.json()))

if __name__ == "__main__":
    unittest.main()