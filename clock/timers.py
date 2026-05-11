import json

TIMER_FILEPATH = "data/timers.json"

def load_timers():
    with open(TIMER_FILEPATH, "r") as file:
        return json.load(file)
