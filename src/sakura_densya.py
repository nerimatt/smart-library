# interact with sakura densya

import requests
from json import dumps

from logger import Logger


def sakura_densya_execute_dict_action(logger: Logger, url: str, action: dict):
    body = dumps(action).encode("utf-8")
    headers = {
        "Content-Type": "application/json",
        "Content-Length": str(len(body)),
        "Connection": "close"
    }

    res = requests.post(url, data = body, headers = headers, parse_headers = False)
    print(res.status_code)
    print(res.text)
    logger.Info(f"sakura densya executing action: {action}")


if __name__ == "__main__":
    from config import conf_load
    from logger import Logger
    from wifi import wifi_connect


    logger = Logger()
    conf = conf_load()

    wifi_connect(logger)

    sakura_densya_execute_dict_action(
        logger,
        conf["sakura_densya_url"],
        {
            "ceiling-brightness": 50,
            "shop-brightness": 50
        }
    )
