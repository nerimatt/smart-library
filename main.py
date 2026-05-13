# this runs after boot.py, there it automativally mounts sd or avoids booting
# here run as if it is booting for sure (easier to test)

from json import load
from machine import ADC, Pin
import sys
from time import sleep
import _thread

from accurate_time import set_time, get_time
from sdcard import mount_sd_card
from wifi import wifi_connect
from config import conf_load
from logger import Logger
import leds
from leds.animation_manager import AnimationManager
from clock.timer_manager import TimerManager

def main():
    logger = Logger()

    conf = conf_load()


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
    cluster_animation_manager = AnimationManager(logger, cluster, conf) # NOTE: create in LED_cluster.anim


    ############## get boot permissions ##############
    # TODO: create button class
    if btn_red.value(): #NOTE: hold red button to avoid booting

        logger.Error("Did not have permissions to boot")
        return


    ############## start ##############
    timer_manager = TimerManager(logger)

    if conf["offline"]:
        logger.Warn("esp is offline (disabled in config). cannot use webservers, and time")
        timer_manager.disable()
    else:
        wifi_connect(logger, conf["debugging"])
        set_time()


    logger.Info("starting")
    leds.cluster_blink(cluster, 3)

    _thread.start_new_thread(timer_manager.loop) # will sleep till timers run out

    cluster_animation_manager.set_animation(AnimationManager.FADE, {"color": (255, 0, 0)})


    while True:
        cluster_animation_manager.step()
        cluster.update()

        sleep(1 / conf["fps"])



if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        sys.print_exception(e)



