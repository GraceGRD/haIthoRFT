"""Constants for the Itho integration."""
# from datetime import timedelta
from logging import Logger, getLogger

# Integration domain
DOMAIN = "itho_remote"

LOGGER: Logger = getLogger(__package__)
# SCAN_INTERVAL = timedelta(seconds=30)
SCAN_INTERVAL = None

# Options

NAME = "Itho RFT Remote"
BRAND = "Itho Daalderop"
MODEL = "RFT AUTO 1,A,3,T (536-0150)"
VERSION = "0.0.0"

CONF_REMOTE_ADDRESS = "remote_address"
CONF_UNIT_ADDRESS = "unit_address"

# TODO: Add icon for custom_integration: https://github.com/home-assistant/brands
