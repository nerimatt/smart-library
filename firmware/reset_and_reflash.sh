# NOTE: run from parent folder

esptool erase-flash &&
esptool --baud 460800 write-flash 0x1000 ./firmware/ESP32_GENERIC-20260406-v1.28.0.bin
