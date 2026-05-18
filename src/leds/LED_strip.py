# Imports
from machine import Pin
from neopixel import NeoPixel

from time import sleep
from random import randint

# NOTE: a lot of methods return self to concat commands
class LED_strip:
    def __init__(self, data_pin, n_leds) -> None:

        # Define the strip pin to GPIO 27 and number of LEDs (15)
        self.strip = NeoPixel(Pin(data_pin), n_leds)

    @property
    def len(self):
        return self.strip.__len__()

    def set(self, pos = 0, col = (0, 0, 0)) -> LED_strip:
        # set color of a particular pixel

        if not 0 <= pos <= self.len:
            print("leds out of range")
            return self

        if max(col) > 255 or min(col) < 0:
            print("colors paramter must be in 0 <= col <= 255")
            return self

        self.strip[pos] = col
        return self

    def fill(self, col = (0, 0, 0)) -> LED_strip:
        self.strip.fill(col)
        return self

    def update(self):
        self.strip.write()


    def off(self):
        self.strip.fill((0, 0, 0))
        self.update()



if __name__ == "__main__":
    strip = LED_strip(data_pin = 13, n_leds = 20)

    strip.fill((255, 255, 255)).set(0, (255, 0, 0)).update()





