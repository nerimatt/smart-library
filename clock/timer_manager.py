import json
import time

from logger import Logger
from accurate_time import get_time

class TimerManager:
    TIMER_FILEPATH = "data/timers.json"
    timers: dict
    _enabled = True

    def __init__(self, logger: Logger):
        self.logger = logger

        with open(TIMER_FILEPATH, "r") as file:
            self.timers = json.load(file)

    def disable(self):
        self._enabled = False

    def enable(self):
        self._enabled = True

    def save_timers(self):
        pass


    def find_next_timer(self):
        pass

    def sleep_till_next_timer(self):
        pass

    def loop(self):
        while True:
            time.sleep(5)




if __name__ == "__main__":

    import wifi
    from logger import Logger

    logger = Logger()
    wifi.wifi_connect(logger)

    set_time()

    timer_manager = TimerManager(logger)
    print(timer_manager.timers)
    print(timer_manager.find_next_timer())
