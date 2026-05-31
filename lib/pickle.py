
ROOT_SAVES = "data/"

def dump(obj: object, filename):
    with open(ROOT_SAVES + filename, "w") as file:
        print(repr(obj))
        file.write(repr(obj))


