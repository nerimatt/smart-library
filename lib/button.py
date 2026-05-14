from machine import Pin

class Button:
    _btn: Pin
    pressed: bool = False

    def __init__(self, pin: int):
        self._btn = Pin(pin, Pin.IN, Pin.PULL_DOWN)

    def update(self):
        self.pressed = self._btn.value()

        # TODO: fix pressing for more frames or holding
        # for now implement cooldown to repress after pressing once (by 0.1 secs)

