"""Itho Coordinator integration using DataUpdateCoordinator."""
from __future__ import annotations

import asyncio

from IthoRFT.remote import IthoRFTRemote

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_PORT
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import DOMAIN, LOGGER, SCAN_INTERVAL, CONF_REMOTE_ADDRESS, CONF_UNIT_ADDRESS


class IthoCoordinator(DataUpdateCoordinator):
    """Itho coordinator."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        """Initialize Itho coordinator."""
        super().__init__(hass, LOGGER, name=DOMAIN, update_interval=SCAN_INTERVAL)

        # Start the IthoRemoteRFT task
        self.remote = IthoRFTRemote(
            port=entry.data[CONF_PORT],
            remote_address=entry.data[CONF_REMOTE_ADDRESS],
            unit_address=entry.data[CONF_UNIT_ADDRESS],
            log_to_file=False,  # TODO: Through config option?
        )
        self.remote.register_data_callback(self.data_updated)
        self.remote.start_task()

    def data_updated(self, data):
        """Update Itho data."""
        self.async_set_updated_data(data)

    async def _async_update_data(self):
        """Fetch data from Itho."""
        self.remote.request_data()

        await asyncio.sleep(1)  # TODO: Wait for completion?
