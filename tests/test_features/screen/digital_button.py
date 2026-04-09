from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

import time

# Set up I2C and the pins we're using for it
i2c = I2C(0,sda=Pin(27), scl=Pin(12), freq=400000)

# Short delay to stop I2C falling over
time.sleep(1) 

HEIGHT = 64
WIDTH = 128

# Define the display and size (128x32)
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Clear the display first
display.fill(0) 

def display_button(msg: str, selected: bool, top_corner: tuple = (0,0), hp: int = 0, vp: int = 0):
    # hp, vp -> horizontal, vertical padding
    TEXT_RES = 8
    
    display.rect(top_corner[0], top_corner[1], TEXT_RES * len(msg) + 2 * hp + 8, TEXT_RES + 6 + 2 * vp, 1)
    
    if selected:
        pass

    # remove borders
    display.pixel(top_corner[0], top_corner[1], 0)
    display.pixel(TEXT_RES * len(msg) + 2 * hp + 7, top_corner[1], 0)
    display.pixel(top_corner[0], top_corner[1] + TEXT_RES + 5 + 2 * vp, 0)
    display.pixel(TEXT_RES * len(msg) + 2 * hp + 7 + top_corner[0], TEXT_RES + 5 + 2 * vp + top_corner[1], 0)
    

    display.text(msg, top_corner[0] + hp + 4, top_corner[1] + vp + 4, not selected)




display_button("Hell0 worlD", False, top_corner = (0, 0), hp = 12, vp = 0)
display_button("Hell0 worlD", True, top_corner = (0, 13), hp = 12, vp = 4)
display_button("Hell0 worlD", False, top_corner = (0, 26 + 8), hp = 12, vp = 0)


# Update the display
display.show()





