import json
import time

from logger import Logger
from accurate_time import set_time, get_time

class DayEnum:
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


class TimerManager:
    TIMER_FILEPATH = "data/timers.json"
    timers: list[dict]
    _enabled = True

    def __init__(self, logger: Logger):
        self.logger = logger

        with open(self.TIMER_FILEPATH, "r") as file:
            self.timers = json.load(file)["timers"]

    def disable(self):
        self._enabled = False

    def enable(self):
        self._enabled = True

    def save_timers(self):
        with open(self.TIMER_FILEPATH, "w") as file:
            self.timers = json.dump({"timers": self.timers}, file, indent = 4)

    def encode_timer(self, month, day, hour, min):
        return month * 10**6 + day * 10**4 + hour * 10**2 + min

    def find_next_timer(self) -> (dict, int):
        t = get_time()

        # convert time now in number from 0000 to 2359
        # encoded <day><hour><min> like -> 22300 -> wednesday 23:00
        t_enc = self.encode_timer(t[1], t[2], t[3], t[4])

        # check if there are numbers greater than the number at our same day
        closest = None
        closest_enc = -9999999999
        closest_t = None
        for timer in self.timers:

            # create encoding for every day of the week and every month
            for t2 in timer["times"]:

                h2 = int(t2.split(":")[0])
                min2 = int(t2.split(":")[1])

                for month in timer.get("months", []):
                    for day in timer.get("days", []):
                        t2_enc = self.encode_timer(month, day, h2, min2)

                        # if t2 is in the future (> 0) and closest, win
                        # FIX: this doesnt wrap around weeks
                        if 0 < t2_enc - t_enc < closest_enc:
                            closest = timer
                            closest_enc = t2_enc
                            closest_t = (t[0], month, day, h2, min2) # FIX: add one year if it wraps around

        return closest, closest_enc


        # get smaller number of next day (if there is not go next day)


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
    # print(timer_manager.timers)
    print(timer_manager.find_next_timer())
