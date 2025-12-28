import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from src.core.constants import DEFAULT_TIMEOUT, DELIVERY_INDICATORS
from src.core.models import Location, Package
from src.trackers.base import CourierTracker

logger = logging.getLogger(__name__)


class CourierCenterTracker(CourierTracker):

    def track(self, tracking_number: str) -> Package:
        """Track a CourierCenter package."""
        package = Package(courier_name="CourierCenter")
        url = f"https://courier.gr/track/result?tracknr={tracking_number}"

        try:
            response = requests.get(url, timeout=DEFAULT_TIMEOUT)
            soup = BeautifulSoup(response.text, "html.parser")

            if soup.find("h4", {"class": "error"}):
                return package

            package.found = True

            rows = soup.find_all("div", {"class": "tr"})

            for row in rows[1:]:
                date_div = row.find("div", {"id": "date"})
                time_div = row.find("div", {"id": "time"})
                area_div = row.find("div", {"id": "area"})
                action_div = row.find("div", {"id": "action"}) or row.find(
                    "div", {"id": "actions"}
                )

                if date_div and time_div:
                    dt_str = f"{date_div.text.strip()} {time_div.text.strip()}"
                    try:
                        dt = datetime.strptime(dt_str, "%d/%m/%Y %H:%M")
                    except ValueError:
                        dt = datetime.now()

                    package.locations.append(
                        Location(
                            datetime=dt,
                            location=area_div.text.strip() if area_div else "",
                            description=action_div.text.strip() if action_div else "",
                        )
                    )

            status_div = soup.find("div", {"class": "status"})
            delivery_indicator = DELIVERY_INDICATORS.get("couriercenter", "")
            if status_div and delivery_indicator in status_div.text:
                package.delivered = True

            return package

        except Exception as e:
            logger.error(f"Error tracking CourierCenter package: {e}")
            return package
