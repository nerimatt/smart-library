import os
import json


def load(filename: string, mode: string):
    data = dict()
    try:
        with open(filename, mode) as file:
            data = json.load(file)

    except OSError as e:
        pass

    return data


def dump(data, filename):
    try:
        parent_folder = "/".join(filename.split("/")[:-1])
        os.mkdir(parent_folder)

    except Exception as e:
        print(e)

    with open(filename, "w") as file:
        json.dump(data, file)

