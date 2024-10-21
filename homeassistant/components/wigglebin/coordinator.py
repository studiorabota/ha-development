"Coordinator for WiggleBin integration."

from datetime import timedelta
import logging

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)


def raise_update_failed(response):
    """Raise an UpdateFailed exception with a message containing the response status."""
    raise UpdateFailed(f"Error fetching data: {response.status}")


class WiggleBinDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching WiggleBin data."""

    def __init__(self, hass: HomeAssistant, api_url) -> None:
        """Initialize."""
        super().__init__(
            hass,
            _LOGGER,
            name="WiggleBin",
            update_interval=timedelta(minutes=5),
            update_method=self._async_update_data,
        )
        self.api_url = api_url

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            async with (
                aiohttp.ClientSession() as session,
                session.get(f"{self.api_url}/sensors/") as response,
            ):
                if response.status != 200:
                    raise_update_failed(response)
                return await response.json()
        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err
