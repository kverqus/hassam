from homeassistant.const import CONF_NAME
from datetime import timedelta

__version__ = "0.0.1"
VERSION = __version__
DOMAIN = "hassam"

DEVICE_NAME = "SSAM Waste Collection"
DEVICE_AUTHOR = "Kristoffer Nilsson"
DEVICE_VERSION = __version__

PLATFORMS = ["sensor"]
SENSOR_ATTRIB = "Data from SSAM (Södra Smålands Avfall och Miljö)"

SCAN_INTERVAL = timedelta(minutes=120)
