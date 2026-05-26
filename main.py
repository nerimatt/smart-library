# this runs after boot.py, there it automativally mounts sd or avoids booting
# here run as if it is booting for sure (easier to test)

from json import load
from machine import ADC, Pin
import sys
from time import sleep
import _thread

from accurate_time import set_time, get_time
from sdcard import mount_sd_card
import wifi
from config import conf_load
from logger import Logger
import src.leds as leds
from src.leds.animation_manager import AnimationManager
from src.clock.timer_manager import TimerManager
from src.sakura_densya import sakura_densya_execute_dict_action

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

    # TODO: do in boot, even logger do it there and find way to make it global, or pass it from boot to main
    accesspoint = wifi.wifi_setup_hotspot(logger, conf["accesspoint"])


    ############## get boot permissions ##############
    # TODO: create button class
    if btn_red.value(): #NOTE: hold red button to avoid booting
        logger.Error("Did not have permissions to boot")
        return


    ############## start ##############
    timer_manager = TimerManager(logger)

    # save action in var so cluster doesnt get modified in parallel
    timer_d = {
        "action": None,
    }
    def timer_manager_loop():
        logger.Info("starting timer manager loop")
        while True:
            timer_d["action"] = timer_manager.sleep_till_next_timer(logger) # will sleep till timers run out


    wifi_station = None
    if conf["offline"]:
        logger.Warn("esp is offline (disabled in config). cannot use webservers, and time")
    else:
        # wifi_station = wifi.wifi_connect(logger, conf["debugging"], True)
        wifi_station = wifi.wifi_connect(logger, conf["debugging"], False)
        if wifi_station: # possible that wifi isnt found
            set_time(logger)
            _thread.start_new_thread(timer_manager_loop, ())
        else:
            logger.Error("could not get a wifi station working")

    # # TODO: works with no problem, to implement the webserver
    # def loop_inf():
    #     while True:
    #         print(12)
    #         sleep(30)
    # print("starnig third thread")
    # _thread.start_new_thread(loop_inf, ())


    logger.Info("starting...")
    leds.cluster_blink(cluster, 3)


    cluster_animation_manager.set_animation(AnimationManager.FADE, {"color": (64, 37, 0)})


    # TODO: add try in loop, and print exceptions exactly.
    # TODO: check once in a while for wifi (every 5 to ten minutes), might help to create timers
    while True:
        if timer_d["action"]:
            if cluster_action := timer_d["action"].get("cluster"):
                leds.cluster_execute_dict_action(cluster, cluster_animation_manager, logger, cluster_action)

            if sakura_action := timer_d["action"].get("sakura_densya"):
                if wifi.wifi_check_station_connection(wifi_station): # TODO: remove when hosting and making sakura connect to out accesspoint
                    sakura_densya_execute_dict_action(logger, conf["sakura_densya_url"], sakura_action)

            timer_d["action"] = None


        cluster_animation_manager.step()

        cluster.update()
        sleep(1 / conf["fps"])



if __name__ == "__main__":
    try:
        main()

    except Exception as e:
        # TODO: save logs
        sys.print_exception(e)



