import logging
from datetime import datetime

import requests

from greek_parcel.core.constants import DEFAULT_TIMEOUT
from greek_parcel.core.models import Location, Package
from greek_parcel.trackers.base import CourierTracker

logger = logging.getLogger(__name__)


class SkroutzTracker(CourierTracker):

    def track(self, tracking_number: str) -> Package:
        """Track a Skroutz package."""
        package = Package(courier_name="Skroutz")
        url = f"https://api.sendx.gr/user/hp/{tracking_number}"

        try:
            response = requests.get(url, timeout=DEFAULT_TIMEOUT)
            if response.status_code >= 400:
                return package

            data = response.json()
            package.found = True

            details = data.get("trackingDetails", [])
            for item in details:
                date_str = item.get("updatedAt", "")
                try:
                    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                except ValueError:
                    dt = datetime.now()

                package.locations.append(
                    Location(
                        datetime=dt,
                        location=item.get("checkpoint", ""),
                        description=item.get("description", ""),
                    )
                )

            if data.get("deliveredAt"):
                package.delivered = True

            return package

        except Exception as e:
            logger.error(f"Error tracking Skroutz package: {e}")
            return package
