# https://docs.micropython.org/en/latest/library/machine.Timer.html
from machine import Pin

from logger import Logger


class Button:
    _logger: Logger

    name: str = ""

    _btn: Pin
    holding_press: bool = False # when button is being hold
    pressed: bool = False

    def __init__(self, logger: Logger, pin: int, name: str):
        self._logger = logger
        self.name = name
        self._btn = Pin(pin, Pin.IN, Pin.PULL_DOWN)

    # override any check if you need the pure pin value at the moment
    def pin_value(self):
        self._btn.value()

    def update(self):
        if self.pressed: # stay active for exactly one frame
            self.reset()

        if self._btn.value():
            self.holding_press = True

        elif self.holding_press: # NOTE: press only on release, if not pressing at the moment but pressed at check before
            self._logger.Debug(f"Button '{self.name}' pressed")
            self.pressed = True
            self.holding_press = False


    def reset(self):
        self.pressed = False
        self._logger.Debug(f"Button '{self.name}' released")

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

