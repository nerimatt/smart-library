# https://chatgpt.com/c/6755694c-e7dc-8010-b6de-3bd9f356aacc

"""
# this in pico
from machine import UART, Pin
import time

# Initialize UART (pins depend on your Pico setup)
uart = UART(0, baudrate=9600, tx=Pin(0), rx=Pin(1))  # Set your TX/RX pins

while True:
    if uart.any():
        data = uart.read().decode('utf-8')  # Read and decode data
        print("Received:", data)
    time.sleep(0.1)
"""


from machine import UART
import time

# Initialize UART (pins depend on your ESP32 setup)
uart = UART(1, baudrate=9600, tx=17, rx=16)  # Set your TX/RX pins

print("sending")
while True:
    uart.write("Hello from ESP32!\n")  # Send data
    time.sleep(1)