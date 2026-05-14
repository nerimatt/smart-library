import time
import ntptime


# account for daylihjt savings
# UTC+1  # CET, winter / standard time
# UTC+2  # CEST, summer / daylight saving time
TIMEZONE = 0
UTC_OFFSET = 0

def _days_in_a_month(year, month):
    if month in (1, 3, 5, 7, 8, 10, 12):
        return 31
    if month in (4, 6, 9, 11):
        return 30
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return 29

    return 28

def _last_sunday(year, month):
    last_day = _days_in_a_month(year, month)
    t = time.mktime((year, month, last_day, 0, 0, 0, 0, 0))
    weekday = time.localtime(t)[6]
    return last_day - ((weekday + 1) % 7)

def _get_italy_timezone(t):
    year = time.localtime(t)[0]

    # ora legale starts last sunday of march at 1:00 utc
    # ends last sunday of october at 1:00 utc
    start_day = _last_sunday(year, 3)
    end_day = _last_sunday(year, 10)

    start = time.mktime((year, 3, start_day, 1, 0, 0, 0, 0))
    end = time.mktime((year, 10, end_day, 1, 0, 0, 0, 0))

    if start <= t < end:
        return 2
    return 1

def _get_utc_offset(timezone: int):
    return timezone * 60 * 60

# NOTE: must be connected to the internet
def set_time():
    global TIMEZONE, UTC_OFFSET

    # ntptime.host = "it.pool.ntp.org" # still returns basic utc
    ntptime.settime()

    # set timezone for italy
    TIMEZONE = _get_italy_timezone(time.time())
    UTC_OFFSET = _get_utc_offset(TIMEZONE)

def get_time():
    # (year, month, day, hour, min, sec 0-61 (includes leap second), week day 0-6, day of year 1-366, should be daylight saving (not present))
    return time.localtime(time.time() + UTC_OFFSET)

if __name__ == "__main__":
    import wifi
    from logger import Logger

    logger = Logger()
    wifi.wifi_connect(logger)

    set_time()
    print(get_time())
