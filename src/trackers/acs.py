import logging
from datetime import datetime

import requests

from src.core.constants import DEFAULT_TIMEOUT, DEFAULT_USER_AGENT
from src.core.models import Location, Package
from src.trackers.base import CourierTracker

logger = logging.getLogger(__name__)


class ACSTracker(CourierTracker):

    def track(self, tracking_number: str) -> Package:
        """Track an ACS package."""
        package = Package(courier_name="ACS")
        url = f"https://api.acscourier.net/api/parcels/search/{tracking_number}"

        try:
            headers = {"User-Agent": DEFAULT_USER_AGENT}
            response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)

            if response.status_code != 200:
                logger.warning(f"ACS returned status code {response.status_code}")
                return package

            data = response.json()
            if not data.get("items"):
                return package

            item = data["items"][0]
            if item.get("notes") == "Η αποστολή δεν βρέθηκε":
                return package

            package.found = True
            package.delivered = item.get("isDelivered", False)

            for point in item.get("statusHistory", []):
                date_str = point.get("controlPointDate")
                if not date_str:
                    continue

                try:
                    dt = datetime.fromisoformat(date_str)
                except ValueError:
                    dt = datetime.now()

                package.locations.append(
                    Location(
                        datetime=dt,
                        location=point.get("controlPoint", ""),
                        description=point.get("description", ""),
                    )
                )

            return package

        except Exception as e:
            logger.error(f"Error tracking ACS package: {e}")
            return package
