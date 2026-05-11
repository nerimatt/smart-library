from config import conf_load
from logger import Logger

logger = Logger()

conf = conf_load()

if conf["mount_sd"]:
    mount_sd_card(logger)
else:
    logger.Info("sd card disabled in config")

