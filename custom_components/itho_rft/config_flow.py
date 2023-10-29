"""Adds config flow for Itho Remote."""
from __future__ import annotations

import asyncio
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PORT
from homeassistant.data_entry_flow import FlowResult

import homeassistant.helpers.config_validation as cv

from IthoRFT.remote import IthoRFTRemote, IthoRemoteGatewayError


from .const import DOMAIN, LOGGER, CONF_REMOTE_ADDRESS, CONF_UNIT_ADDRESS


class IthoRemoteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Itho Remote config flow."""

    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1
    data = None

    async def async_step_user(self, user_input=None):
        """Handle a flow initialized by the user."""
        self.data = []
        return await self.async_step_connect(user_input)

    async def async_step_connect(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle connect evofw3 gateway."""
        errors: dict[str, str] = {}
        if user_input is not None:
            self.remote = IthoRFTRemote(port=user_input.get(CONF_PORT))
            try:
                self.remote.self_test()
            except IthoRemoteGatewayError as exception:
                LOGGER.error(exception)
                errors["base"] = "connection"
            else:
                # Input is valid, set data.
                self.data = user_input
                self.data[CONF_PORT] = user_input.get(CONF_PORT)

            # Success, return the form of the next step
            return await self.async_step_pair_menu()

        return self.async_show_form(
            step_id="connect",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_PORT): cv.string,
                }
            ),
        )

    async def async_step_pair_menu(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle pair menu choice."""
        if user_input is not None:
            LOGGER.warning("async_step_pair_menu: %s", user_input)

        return self.async_show_menu(
            step_id="pair_menu",
            menu_options=["auto_pair", "manual_pair"],
        )

    async def async_step_auto_pair(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle automatic pairing."""
        if user_input is not None:
            self.remote.start_task()
            self.remote.pair()

            # TODO how to wait for completion?
            while self.remote.is_pairing:
                await asyncio.sleep(1)

            LOGGER.debug(
                "pairing done: %s %s",
                self.remote.remote_address,
                self.remote.unit_address,
            )

            # TODO what about pairing failed/timeout?
            self.data[CONF_REMOTE_ADDRESS] = self.remote.remote_address
            self.data[CONF_UNIT_ADDRESS] = self.remote.unit_address

            return await self.async_step_finish()

        return self.async_show_form(
            step_id="auto_pair",
        )

    async def async_step_manual_pair(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle manual pairing."""
        if user_input is not None:
            LOGGER.debug(
                "pairing configured: %s %s",
                user_input.get(CONF_REMOTE_ADDRESS),
                user_input.get(CONF_UNIT_ADDRESS),
            )

            self.data[CONF_REMOTE_ADDRESS] = user_input.get(CONF_REMOTE_ADDRESS)
            self.data[CONF_UNIT_ADDRESS] = user_input.get(CONF_UNIT_ADDRESS)

            return await self.async_step_finish()

        return self.async_show_form(
            step_id="manual_pair",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_REMOTE_ADDRESS): cv.string,
                    vol.Required(CONF_UNIT_ADDRESS): cv.string,
                }
            ),
        )

    async def async_step_finish(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle finish."""

        if user_input is not None:
            LOGGER.debug("Finish: %s", self.data)
            self.remote.stop_task()
            # TODO: Validate addresses (inside pyIthoRFT)?
            return self.async_create_entry(
                title=f"Itho Remote on {self.data[CONF_PORT]}",
                data=self.data,
            )

        return self.async_show_form(
            step_id="finish",
            data_schema=vol.Schema({}),
            description_placeholders={
                "port": self.data[CONF_PORT],
                "remote_address": self.data[CONF_REMOTE_ADDRESS],
                "unit_address": self.data[CONF_UNIT_ADDRESS],
            },
        )
