import network
from utime import sleep
import json

from logger import Logger

WIFI_JSON_PATH = "data/wifis.json"

def wifi_check_station_connection(station: network.WLAN) -> Bool:
    return station and station.isconnected()

def wifi_connect(logger: Logger, verbose = False, force = False) -> network.WLAN:

    with open(WIFI_JSON_PATH, "r") as wififile:
        WIFI_DATA = json.load(wififile) # (SSID, PASSWORD)


    station = network.WLAN(network.STA_IF)
    station.active(True)

    if not force and station.isconnected():
        logger.Info(f"already connected at wifi: '{station.config("ssid")}'")
        return station

    # get available networks
    available_networks = []
    tries = 5
    while tries > 0:
        available_networks = [network[0].decode() for network in station.scan()]

        if available_networks: break
        else:
            logger.Debug("no wifi found... \nretrying...")
            tries -= 1
            sleep(2)


    if verbose:
        logger.Debug(f"available networks: {available_networks}")


    connected = False
    for wifi in WIFI_DATA:
        if wifi not in available_networks: continue


        # Connect to Wi-Fi
        try:
            station.connect(wifi, WIFI_DATA[wifi])
            # Wait for the Wi-Fi connection
            while not station.isconnected():
                sleep(0.2)

            logger.Info(f"connected to {wifi}, ip: {station.ifconfig()[0]}")
            connected = True

            break

        except OSError as e:
            # this is only to ignore impossibility to connect to wifi
            if e.args[0] != "Wifi Internal Error":
                raise e

            if verbose:
                logger.Info(f"cannot connect to '{wifi}'")
            station.disconnect()  # Disconnect before moving to the next network
            station.active(False)  # Disable Wi-Fi interface
            sleep(1)  # Give some time for cleanup and reinitialization
            station.active(True)

    if not connected: logger.Error("couldnt connect to any wifi")

    return station

def wifi_disconnect(station: network.WLAN):
    station.disconnect()  # Disconnect before moving to the next network
    station.active(False)  # Disable Wi-Fi interface



if __name__ == "__main__":
    logger = Logger()
    station = wifi_connect(logger, True)

    import urequests
    response = urequests.get('http://192.168.1.161:8000/anime')
    print(response.content.decode()[:100])

    wifi_disconnect(station)



