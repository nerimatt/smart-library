from json import load, dumps

def conf_load():
    with open("config.json", "r") as file:
        config = load(file)
    return config

def conf_print(conf):
    print(dumps(data, indent = 4))


if __name__ == "__main__":
    conf = conf_load()
    conf_print(conf)
