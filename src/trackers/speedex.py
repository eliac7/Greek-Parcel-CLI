import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from src.core.constants import DEFAULT_TIMEOUT, DELIVERY_INDICATORS
from src.core.models import Location, Package
from src.trackers.base import CourierTracker

logger = logging.getLogger(__name__)


class SpeedexTracker(CourierTracker):

    def track(self, tracking_number: str) -> Package:
        """Track a Speedex package."""
        package = Package(courier_name="Speedex")
        url = f"http://www.speedex.gr/speedex/NewTrackAndTrace.aspx?number={tracking_number}"

        try:
            response = requests.get(url, timeout=DEFAULT_TIMEOUT)
            soup = BeautifulSoup(response.text, "html.parser")

            if soup.find("div", {"class": "alert-warning"}):
                return package

            package.found = True

            cards = soup.find_all("div", {"class": "timeline-card"})
            for card in cards:
                title = card.find("h4", {"class": "card-title"})
                small = card.find("span", {"class": "font-small-3"})

                description = title.text.strip() if title else ""

                location = ""
                dt = datetime.now()

                if small and small.contents:
                    text_content = small.text.strip()
                    parts = text_content.split(", ")
                    if len(parts) >= 2:
                        location = parts[0]
                        date_raw = parts[1]
                        try:
                            dt = datetime.strptime(date_raw, "%d/%m/%Y στις %H:%M")
                        except ValueError:
                            pass

                package.locations.append(
                    Location(datetime=dt, location=location, description=description)
                )

            delivery_indicator = DELIVERY_INDICATORS.get("speedex", "")
            if (
                package.locations
                and package.locations[-1].description == delivery_indicator
            ):
                package.delivered = True

            return package

        except Exception as e:
            logger.error(f"Error tracking Speedex package: {e}")
            return package
