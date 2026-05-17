import json
import time

with open("../../../data/timers.json", "r") as file:
    timers = json.load(file)["timers"]


def encode_timer( month, day, hour, min):
    return month * 10**6 + day * 10**4 + hour * 10**2 + min

# https://tutorialreference.com/python/examples/faq/python-how-to-find-ones-tens-hundreds-thousands-digits
def decode_timer( timer_enc: int):
    pass

def find_next_timer():
    t = time.localtime()
    t = t[:-1]
    print("current time: ", end = "")
    print(f"{t[2]}/{t[1]}/{t[0]} at {t[3]}:{t[4]}")

    # convert time now in number from 0000 to 2359
    # encoded <month><day><hour><min> like -> 122300 -> feb wednesday 23:00
    t_enc = encode_timer(t[1], t[6], t[3], t[4])
    print(f"current time encoding: {t_enc}")

    # check if there are numbers greater than the number at our same day
    closest = None
    closest_diff = 99999999999
    closest_enc = None

    # get only enabled timers
    timers_filt = filter(lambda x: x.get("enabled", False), timers)

    for timer in timers_filt:

        # create encoding for every day of the week and every month
        for (h2, min2) in timer["times"]:

            for month in timer.get("months", []):
                for day in timer.get("days", []):
                    t2_enc = encode_timer(month, day, h2, min2)

                    # if t2 is in the future (> 0) and closest, win
                    diff = t2_enc - t_enc

                    # timer is in the past, add one week or year
                    # we dont care we "overflow" days and months, comparison is gonna be the same
                    # TODO: test
                    if diff < 0:
                        # if days is bigger, add one week (+ 7 * 10^4)
                        if day > t[2]:
                            t2_enc += encode_timer(0, 7, 0, 0)


                        # if month is bigger, add one year
                        if month > t[1]:
                            t2_enc += encode_timer(12, 0, 0, 0)


                    # new closest
                    if 0 < diff < closest_diff:
                        closest_diff = diff
                        closest = timer
                        closest_enc = t2_enc

    return closest, closest_enc


    # get smaller number of next day (if there is not go next day)


    def sleep_till_next_timer():
        pass


if __name__ == "__main__":

    tmr, t = find_next_timer()

    print("res: ", end = "")
    print(tmr, t)

