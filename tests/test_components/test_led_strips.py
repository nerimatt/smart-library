# Imports
from machine import Pin
from neopixel import NeoPixel

from time import sleep
from random import randint

from RGBSTRIP import RGBSTRIP

leds_per_segment = 20
segments = 8

PIN_STRIP_1 = 12
PIN_STRIP_2 = 13

strip = RGBSTRIP(data_pin = PIN_STRIP_1, n_leds = segments * leds_per_segment)
strip2 = RGBSTRIP(data_pin = PIN_STRIP_2, n_leds = segments * leds_per_segment)
#strip = RGBSTRIP(data_pin = 13, n_leds = legs_per_segment)

def get_random_color():
    return (randint(0, 255), randint(0, 255), randint(0, 255))
 
print("testing leds")
while True: # Run forever
    col = get_random_color()
    
    strip.fade(col)
    #strip2.fade(col)
    #strip.fade(color = (255, 255, 255))
    
    #strip.led_chase(bg_color = get_random_color(), snake_color = get_random_color(), snake_len = randint(1, 5))

    
