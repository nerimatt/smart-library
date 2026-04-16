from json import load
from machine import ADC, Pin
import logger
import sys

logger = logger.Logger()

with open("config.json", "r") as file:
    conf = load(file)
    print(conf)

if not conf["boot"]:
    logger.Info("Boot disabled in config, exiting")
    sys.exit()


############## load io and sensors ##############
logger.Info("loading all IO and sensors")

btn_red = Pin(conf["io"]["pin_button_red"], Pin.IN, Pin.PULL_DOWN)
btn_green = Pin(conf["io"]["pin_button_green"], Pin.IN, Pin.PULL_DOWN)

potentiometer = ADC(Pin(conf["io"]["pin_potentiometer"]))
potentiometer.atten(ADC.ATTN_11DB) # set adc attenuation to full 3.3v

############## get boot permissions ##############
if btn_red.value(): #NOTE: hold red button to avoid booting

    logger.Error("Did not have permissions to boot")
    sys.exit()

logger.Info("Booting up")

############## start ##############

#import tests.test_components.screen
#import tests.test_components.test_led_strips.py

