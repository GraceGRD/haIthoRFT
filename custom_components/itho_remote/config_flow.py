"""Adds config flow for Itho Remote."""
from __future__ import annotations

import asyncio

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PORT
from homeassistant.data_entry_flow import FlowResult

import homeassistant.helpers.config_validation as cv

from .itho_remote import IthoRemoteRFT, IthoRemoteGatewayError

from .const import DOMAIN, CONF_REMOTE_ADDRESS, CONF_UNIT_ADDRESS


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
        if user_input is not None:
            # TODO: Attempt a connect
            print("async_step_connect result")
            print(user_input)

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
            # TODO: Decide, or remove async_step_pair_menu and show menu in async_step_connect
            print("async_step_pair_menu result")
            print(user_input)

        return self.async_show_menu(
            step_id="pair_menu",
            menu_options=["auto_pair", "manual_pair"],
        )

    async def async_step_auto_pair(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle automatic pairing."""
        if user_input is not None:
            # TODO: Perform pairing
            print("async_step_auto_pair :)")
            print(user_input)

            await asyncio.sleep(5)

            return await self.async_step_finish()

        return self.async_show_form(
            step_id="auto_pair",
        )

    async def async_step_manual_pair(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle manual pairing."""
        if user_input is not None:
            # TODO: Validate addresses (inside pyIthoRFT)?
            print("async_step_manual_pair :)")
            print(user_input)

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
        print("async_step_finish")
        print(user_input)
        print(self.data)

        if user_input is not None:
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

    # async def _test_gateway_communication(self, port) -> None:
    #     """Validate gateway communication."""
    #     itho_remote = IthoRemoteRFT(port=port)
    #     itho_remote.self_test(itho_remote.evofw3_min_version)
