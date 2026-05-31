import json
import time
from machine import Timer

from logger import Logger
from accurate_time import set_time, get_time, get_timezone

import datetime

class DayEnum:
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6

weekdays = [
    "monday",
    "tuesday",
    "wednesday",
    "thursday",
    "friday",
    "saturday",
    "sunday",
]

months = [
    "january",
    "febuary",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december"
]

class TimerManager:
    TIMER_FILEPATH = "data/timers.json"
    timers: list[dict]
    _timer: Timer

    def __init__(self, logger: Logger):
        self.logger = logger

        with open(self.TIMER_FILEPATH, "r") as file:
            self.timers = json.load(file)["timers"]

    def save_timers(self):
        with open(self.TIMER_FILEPATH, "w") as file:
            self.timers = json.dump({"timers": self.timers}, file, indent = 4)

    def encode_timer(self, month, day, hour, min):
        return month * 10**6 + day * 10**4 + hour * 10**2 + min

    # https://tutorialreference.com/python/examples/faq/python-how-to-find-ones-tens-hundreds-thousands-digits
    def decode_timer(self, timer_enc: int):
        return (
            timer_enc % 10**8 // 10**6,
            timer_enc % 10**6 // 10**4,
            timer_enc % 10**4 // 10**2,
            timer_enc % 100
        )

    def prettify_encoding(self, timer_enc: int) -> str:
        month, day, hour, minute = self.decode_timer(timer_enc)
        return f"{months[month - 1]} {weekdays[day]} at {hour}:{minute:02d}"

    def find_next_timer(self):
        t = get_time()

        # convert time now in number from 0000 to 2359
        # encoded <month><day><hour><min> like -> 122300 -> feb wednesday 23:00
        t_month = t[1]
        t_weekday = t[6]
        t_hour = t[3]
        t_min = t[4]
        t_enc = self.encode_timer(t_month, t_weekday, t_hour, t_min)
        # print(f"current time encoding: {t_enc}")

        # check if there are numbers greater than the number at our same day
        closest = None
        closest_diff = 99999999999
        closest_enc = None

        # get only enabled timers
        timers_filt = filter(lambda x: x.get("enabled", False), self.timers)

        for timer in timers_filt:

            # create encoding for every day of the week and every month
            for (h2, min2) in timer["times"]:
                for month in timer.get("months", []):
                    for day in timer.get("days", []):
                        t2_enc = self.encode_timer(month, day, h2, min2)
                        cmp_enc = t2_enc # copy to modify

                        # if t2 is in the future (> 0) and closest, win
                        diff = cmp_enc - t_enc

                        # if we hit timer on exact hour and minute, skip it
                        if diff == 0:
                            continue

                        # timer is in the past, add one week or year
                        # we dont care we "overflow" days and months, comparison is gonna be the same
                        # TODO: test
                        if diff < 0:
                            if month < t_month:
                                cmp_enc += self.encode_timer(12, 0, 0, 0) # add one year



                            # if days is smaller than now, add one week (+ 7 * 10^4)
                            if day < t_weekday:
                                cmp_enc += self.encode_timer(0, 7, 0, 0)

                            diff = cmp_enc - t_enc # recalculate diff

                        # new closest
                        if 0 < diff < closest_diff:
                            closest_diff = diff
                            closest = timer
                            closest_enc = t2_enc

        return closest, closest_enc


    # seconds it will take to arrive to timer
    def seconds_till_timer(self, timer: dict, timer_enc: int):
        t = get_time()
        timer_v = self.decode_timer(timer_enc)

        # find datetime for timer_v

        now = datetime.datetime(t[0], t[1], t[2], t[3], t[4], t[5])
        start = now.toordinal()
        target = None

        # NOTE: this doesnt account for changing timezones in between timers,
        # next timer over change will readjust

        # try for all days in a year
        for i in range(366):
            d = datetime.date.fromordinal(start + i)

            # find first matching occurence
            if d.month == timer_v[0] and d.weekday() == timer_v[1]:
                target = datetime.datetime(
                    d.year, d.month, d.day,
                    timer_v[2], timer_v[3],
                )
                break

        return int((target - now).total_seconds())

    def sleep_till_next_timer(self, logger) -> dict:
        timer, timer_enc = self.find_next_timer()
        seconds_to_sleep = self.seconds_till_timer(timer, timer_enc)

        logger.Info(f"setting timer '{timer.get("id", 'err')}' for: {self.prettify_encoding(timer_enc)}, in {seconds_to_sleep / 60} minutes")
        time.sleep(seconds_to_sleep)
        logger.Info(f"timer '{timer.get("id", 'err')}' finished")

        return timer.get("action", {})





if __name__ == "__main__":

    import wifi
    from logger import Logger

    logger = Logger()
    wifi.wifi_connect(logger)

    set_time()

    timer_manager = TimerManager(logger)
    # print(timer_manager.timers)
    next_timer, next_timer_enc = timer_manager.find_next_timer()
    print(next_timer)
    print(timer_manager.decode_timer(next_timer_enc))

    print("sleep for seconds:", timer_manager.seconds_till_timer(next_timer, next_timer_enc))
