import logging
from datetime import datetime

import requests

from src.core.constants import DEFAULT_TIMEOUT, DELIVERY_INDICATORS
from src.core.models import Location, Package
from src.trackers.base import CourierTracker

logger = logging.getLogger(__name__)


class EltaTracker(CourierTracker):

    def track(self, tracking_number: str) -> Package:
        """Track an ELTA package."""
        package = Package(courier_name="ELTA")
        url = "https://www.elta-courier.gr/track.php"

        try:
            response = requests.post(
                url, data={"number": tracking_number}, timeout=DEFAULT_TIMEOUT
            )
            data = response.json()

            if "result" not in data or tracking_number not in data["result"]:
                return package

            package_data = data["result"][tracking_number]
            if package_data.get("status") == 0:
                return package

            package.found = True

            history = package_data.get("result", [])
            for item in history:
                date_str = f"{item['date']} {item['time']}"
                try:
                    dt = datetime.strptime(date_str, "%d-%m-%Y %H:%M")
                except ValueError:
                    try:
                        dt = datetime.strptime(date_str, "%d-%m-%Y %H:")
                    except ValueError:
                        dt = datetime.now()

                package.locations.append(
                    Location(
                        datetime=dt,
                        location=item.get("place", ""),
                        description=item.get("status", ""),
                    )
                )

            delivery_indicator = DELIVERY_INDICATORS.get("elta", "")
            if (
                package.locations
                and package.locations[-1].description == delivery_indicator
            ):
                package.delivered = True

            return package

        except Exception as e:
            logger.error(f"Error tracking ELTA package: {e}")
            return package
