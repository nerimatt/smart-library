# Imports
from machine import Pin
from neopixel import NeoPixel

from time import sleep
from random import randint

class RGBSTRIP:
    def __init__(self, data_pin, n_leds) -> None:

        # Define the strip pin to GPIO 27 and number of LEDs (15)
        self.strip = NeoPixel(Pin(data_pin), n_leds)

    @property
    def len(self):
        return self.strip.__len__()

    def set(self, pos = 0, col = (0, 0, 0)):
        # set color of a particular pixel
    
        if not 0 <= pos <= self.len:
            print("leds out of range")
            return
        if max(col) > 255 or min(col) < 0:
            print("colors paramter must be in 0 <= col <= 255")
            return

        self.strip[pos] = col
        return self

    def write(self):
        self.strip.write()

    def fill(self, col = (0, 0, 0)):
        self.strip.fill(col)
        return self

    def off(self):
        self.strip.fill((0, 0, 0))
        self.strip.write()
    
    def fade(self, color = (255, 255, 255), step = 400, delay = 0.005):
        # Iterate from 1 to 255 in steps of 1
        for i in range(1, step, 1):
            
            # Fill the strip using the iterated R value
            self.strip.fill([ int( x / step * i ) for x in color ])
            
            self.strip.write()
            sleep(delay)
            
        # # iterate from 255 to 1 in steps of -1
        for i in range(step,1,-1):
            
            # Fill the strip using the iterated R value
            self.strip.fill([ int( x / step * i ) for x in color ])
            
            self.strip.write()
            sleep(delay)
    
    def led_chase(self, bg_color = (255, 255, 255), snake_color = (0, 0, 0), snake_len = 1, delay = 0.05):
        # one cycle of snake passing

        self.strip.fill(bg_color)

        for i in range(self.len):
            
            # Set each LED in the range to red
            self.strip[i] = snake_color

            # remove tail from previous cycle
            self.strip[i - snake_len] = bg_color
            
            sleep(delay)
            self.strip.write()

    def magma_flow(self):
        # like a led chaser, but with multiple moving snakes
        # all snakes

        pass


if __name__ == "__main__":
    strip = RGBSTRIP(data_pin = 13, n_leds = 20)

    while True: # Run forever
        strip.fade(color = (255, 255, 255))

        #strip.led_chase(bg_color = rand_cs, snake_color = get_random_color(), snake_len = randint(1, 5))

    



