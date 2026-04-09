# BUTTONS


# Imports
from machine import Pin
import time

# Set up our button names and GPIO pin numbers
# Also set pins as inputs and use pull downs
greenbtn = Pin(33, Pin.IN, Pin.PULL_DOWN)
redbtn = Pin(32, Pin.IN, Pin.PULL_DOWN)


while True: # Loop forever
    
    time.sleep(0.2) # Short Delay
        
    if greenbtn.value() == 1:
        print("green button pressed")
    
    if redbtn.value() == 1:
        print("red button pressed")
     