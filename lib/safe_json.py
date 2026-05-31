import json


def load(filename: string, mode: string):
    data = dict()
    try:
        with open(filename, mode) as file:
            data = json.load(file)

    except OSError as e:
        pass

    return data
