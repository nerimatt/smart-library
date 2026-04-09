from machine import Pin, ADC
import time
 
adc = ADC(Pin(14))
 
while True:
     print(adc.read_u16()/65535*100)
     time.sleep(1)