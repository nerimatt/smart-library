# # Imports
from machine import ADC, Pin
import time

# # Set up the potentiometer on ADC pin 27
potentiometer = ADC(Pin(35))

potentiometer.atten(ADC.ATTN_11DB) # set adc attenuation to full 3.3v

while True: # Loop forever

    print(potentiometer.read_u16() / 655535 * 100) # Read the potentiometer value

    time.sleep(0.2) # Wait a second


