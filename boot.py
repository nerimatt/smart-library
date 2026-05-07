from json import load
from machine import ADC, Pin
import sys
from time import sleep

from sdcard import mount_sd_card
from wifi import wifi_connect
from config import conf_load
from logger import Logger
import leds
from leds.animation_manager import Animation_Manager

def main():
    logger = Logger()

    conf = conf_load()

    if conf["mount_sd"]:
        mount_sd_card(logger)
    else:
        logger.Info("sd card disabled in config")

    if not conf["boot"]:
        logger.Info("Boot disabled in config, exiting")
        return


    ############## load io and sensors ##############
    logger.Info("loading all IO and sensors")

    btn_red = Pin(conf["io"]["pin_button_red"], Pin.IN, Pin.PULL_DOWN)
    btn_green = Pin(conf["io"]["pin_button_green"], Pin.IN, Pin.PULL_DOWN)

    potentiometer = ADC(Pin(conf["io"]["pin_potentiometer"]))
    potentiometer.atten(ADC.ATTN_11DB) # set adc attenuation to full 3.3v

    cluster = leds.cluster_create(conf)
    cluster_animation_manager = Animation_Manager(logger, cluster, conf)


    ############## get boot permissions ##############
    if btn_red.value(): #NOTE: hold red button to avoid booting

        logger.Error("Did not have permissions to boot")
        return

    logger.Info("Booting up")


    ############## start ##############
    if not conf["offline"]: wifi_connect(logger, conf["debugging"])

    leds.cluster_blink(cluster, 3)

    #import tests.test_components.screen
    # import tests.test_components.test_led_strips.py
    # import tests.test_components.test_led_cluster

    cluster_animation_manager.set_animation(Animation_Manager.FADE, {"color": (255, 0, 0)})


    while True:
        cluster_animation_manager.step()
        cluster.update()

        sleep(1 / conf["fps"])



if __name__ == "__main__":
    main()

