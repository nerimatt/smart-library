from time import sleep

from config import conf_load

conf = conf_load()

btn_red = Pin(conf["io"]["pin_button_red"], Pin.IN, Pin.PULL_DOWN)
btn_green = Pin(conf["io"]["pin_button_green"], Pin.IN, Pin.PULL_DOWN)

potentiometer = ADC(Pin(conf["io"]["pin_potentiometer"]))
potentiometer.atten(ADC.ATTN_11DB) # set adc attenuation to full 3.3v



while True:

    print("potentiometer: ", potentiometer.read_u16() / 65535 * 100) # Read the potentiometer value

    if btn_green.value() == 1:
        print("green button pressed")

    if btn_red.value() == 1:
        print("red button pressed")

    sleep(0.2)
