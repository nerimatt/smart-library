import json

CONFIG_FILEPATH = "config.json"

def conf_load():
    with open(CONFIG_FILEPATH, "r") as file:
        return json.load(file)

def conf_print(conf):
    print(json.dumps(conf, indent = 4))


if __name__ == "__main__":
    conf = conf_load()
    conf_print(conf)
