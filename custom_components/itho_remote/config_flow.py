"""Adds config flow for Itho Remote."""
from __future__ import annotations

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_PORT
from homeassistant.helpers import selector

from .itho_remote import IthoRemoteRFT, IthoRemoteGatewayError

from .const import DOMAIN, LOGGER


class IthoRemoteConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Itho Remote config flow."""

    # The schema version of the entries that it creates
    # Home Assistant will call your migrate method if the version changes
    VERSION = 1

    async def async_step_user(
        self, user_input: dict | None = None
    ) -> config_entries.FlowResult:
        """Handle a flow initialized by the user."""
        _errors = {}
        if user_input is not None:
            try:
                await self._test_gateway_communication(port=user_input[CONF_PORT])
            except IthoRemoteGatewayError as exception:
                LOGGER.warning(exception)
                _errors["base"] = "connection"
            else:
                return self.async_create_entry(
                    title=user_input[CONF_PORT],
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_PORT,
                        default=(user_input or {}).get(CONF_PORT),
                    ): selector.TextSelector(
                        selector.TargetSelectorConfig(
                            type=selector.TextSelectorType.TEXT
                        ),
                    ),
                }
            ),
            errors=_errors,
        )

    async def _test_gateway_communication(self, port) -> None:
        """Validate gateway communication."""
        itho_remote = IthoRemoteRFT(port=port)
        itho_remote.test()
