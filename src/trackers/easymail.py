import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from src.core.constants import DEFAULT_TIMEOUT, DELIVERY_INDICATORS
from src.core.models import Location, Package
from src.trackers.base import CourierTracker

logger = logging.getLogger(__name__)


class EasyMailTracker(CourierTracker):

    def track(self, tracking_number: str) -> Package:
        """Track an EasyMail package."""
        package = Package(courier_name="EasyMail")
        url = f"https://trackntrace.easymail.gr/{tracking_number}"

        try:
            response = requests.get(url, timeout=DEFAULT_TIMEOUT)
            soup = BeautifulSoup(response.text, "html.parser")

            if soup.find("div", {"class": "cus-alert"}):
                return package

            tbodies = soup.find_all("tbody")
            if len(tbodies) < 2:
                return package

            body = tbodies[1]
            package.found = True

            current_locations = []
            for row in body.find_all("tr"):
                cols = row.find_all("td")
                if len(cols) < 3:
                    continue

                date_str = cols[0].text.strip()

                try:
                    dt = datetime.strptime(date_str, "%d/%m/%Y %H:%M:%S")
                except ValueError:
                    try:
                        dt = datetime.strptime(date_str[:19], "%d/%m/%Y %H:%M:%S")
                    except ValueError:
                        dt = datetime.now()

                desc = cols[1].text.strip()
                loc = cols[2].text.strip()

                current_locations.append(
                    Location(datetime=dt, location=loc, description=desc)
                )

            package.locations = current_locations[::-1]

            delivery_indicator = DELIVERY_INDICATORS.get("easymail", "")
            if (
                package.locations
                and package.locations[-1].description == delivery_indicator
            ):
                package.delivered = True

            return package

        except Exception as e:
            logger.error(f"Error tracking EasyMail package: {e}")
            return package
