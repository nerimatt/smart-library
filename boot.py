from json import load
from machine import ADC, Pin
import sys

import logger
# import leds

def main():
    logger = logger.Logger()

    with open("config.json", "r") as file:
        conf = load(file)
        print(conf)

    if not conf["boot"]:
        logger.Info("Boot disabled in config, exiting")
        return


    ############## load io and sensors ##############
    logger.Info("loading all IO and sensors")

    btn_red = Pin(conf["io"]["pin_button_red"], Pin.IN, Pin.PULL_DOWN)
    btn_green = Pin(conf["io"]["pin_button_green"], Pin.IN, Pin.PULL_DOWN)

    potentiometer = ADC(Pin(conf["io"]["pin_potentiometer"]))
    potentiometer.atten(ADC.ATTN_11DB) # set adc attenuation to full 3.3v

    # cluster = leds.cluster_create(conf)


    ############## get boot permissions ##############
    if btn_red.value(): #NOTE: hold red button to avoid booting

        logger.Error("Did not have permissions to boot")
        return

    logger.Info("Booting up")


    ############## start ##############
    # leds.cluster_blink(cluster, 3)

    #import tests.test_components.screen
    # import tests.test_components.test_led_strips.py
    # import tests.test_components.test_led_cluster

if __name__ == "__main__":
    main()

