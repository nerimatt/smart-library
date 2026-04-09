from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

import time

# Set up I2C and the pins we're using for it
i2c = I2C(0,sda=Pin(27), scl=Pin(14), freq=400000)

# Short delay to stop I2C falling over
time.sleep(1) 

HEIGHT = 64
WIDTH = 128

# Define the display and size (128x32)
display = SSD1306_I2C(WIDTH, HEIGHT, i2c)

# Clear the display first
display.fill(0) 

# # Write a line of text to the display
display.text("Hello World!",0,0)

# write dot to display
# display.pixel(25, 30, 1)


# draw micropython logo

# display.fill(0)
# display.fill_rect(0, 0, 32, 32, 1)
# display.fill_rect(2, 2, 28, 28, 0)
# display.vline(9, 8, 22, 1)
# display.vline(16, 2, 22, 1)
# display.vline(23, 8, 22, 1)
# display.fill_rect(26, 24, 2, 4, 1)
# display.text('MicroPython', 40, 0, 1)
# display.text('SSD1306', 40, 12, 1)
# display.text('OLED 128x64', 40, 24, 1)

from math import sin, cos, pi, radians

# sin(90) sta y = 32 come sin(x) sta a y

xplane_pos = int(HEIGHT / 2)

# draw sine wave
for x in range(WIDTH + 1):
    y = int( sin( 2 * pi * (x / WIDTH) ) * xplane_pos )
    print(x, y, sep = " - ")
    display.pixel(x, xplane_pos + y, 1)
    



# Update the display
display.show()
