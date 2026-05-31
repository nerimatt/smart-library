# https://docs.micropython.org/en/latest/library/machine.Timer.html
from machine import Pin, Timer

from logger import Logger


class Button:
    _logger: Logger

    name: str = ""

    _btn: Pin
    holding_press: bool = False # when button is being hold
    pressed: bool = False

    # NOTE: each button uses a hardware timer, esp supports max 4 of them
    # if needing to use a timer in some other process, remove it from here or it will be overridden
    BTN_FIRST_ID = 1 # ill leave the id 0 free for now
    BTN_MAX_ID = 3
    _free_id: int = BTN_FIRST_ID # static global counter
    id: int
    _tmr: Timer
    COOLDOWN_MS = 200

    def __init__(self, logger: Logger, pin: int, name: str):
        self._logger = logger
        self.name = name
        self._btn = Pin(pin, Pin.IN, Pin.PULL_DOWN)

        if self._free_id > self.BTN_MAX_ID:
            logger.Error("hardware timers finished, cannot create any more, this button is useless")
            return

        self.id = self._free_id
        self._tmr = Timer(self.id)
        Button._free_id += 1

    # override any check if you need the pure pin value at the moment
    def pin_value(self):
        self._btn.value()

    def update(self):
        if self.pressed: return # avoid spam before timer finished

        if self._btn.value():
            self.holding_press = True

        elif self.holding_press: # NOTE: press only on release, if not pressing at the moment but pressed at check before
            self._logger.Debug(f"Button '{self.name}' pressed")
            self.pressed = True
            self.holding_press = False
            self._tmr.init(mode = Timer.ONE_SHOT, period = self.COOLDOWN_MS, callback = self.reset)


    def reset(self, t: Timer):
        self.pressed = False
        self._logger.Debug(f"Button timer '{self.name}' finished")

if __name__ == "__main__":
    from time import sleep
    from logger import Logger
    from config import conf_load

    logger = Logger()
    conf = conf_load()

    grn_btn = Button(logger, conf["io"]["pin_button_green"], "green")
    red_btn = Button(logger, conf["io"]["pin_button_red"], "red")

    while True:
        grn_btn.update()
        red_btn.update()
        sleep(1/conf["fps"])

