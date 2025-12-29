"""Geniki Taxydromiki courier tracker implementation."""

import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from greek_parcel.core.constants import DEFAULT_TIMEOUT
from greek_parcel.core.models import Location, Package
from greek_parcel.trackers.base import CourierTracker

logger = logging.getLogger(__name__)


class GenikiTracker(CourierTracker):
    """Tracker for Geniki Taxydromiki courier service."""

    def track(self, tracking_number: str) -> Package:
        """Track a Geniki Taxydromiki package."""
        package = Package(courier_name="Geniki Taxydromiki")
        url = f"https://www.taxydromiki.com/track/{tracking_number}"

        try:
            response = requests.get(url, timeout=DEFAULT_TIMEOUT)
            soup = BeautifulSoup(response.text, "html.parser")

            if soup.find("div", {"class": "empty-text"}):
                return package

            package.found = True

            checkpoints = soup.find_all("div", {"class": "tracking-checkpoint"})
            for ckpt in checkpoints:
                status_div = ckpt.find("div", {"class": "checkpoint-status"})
                location_div = ckpt.find("div", {"class": "checkpoint-location"})
                date_div = ckpt.find("div", {"class": "checkpoint-date"})
                time_div = ckpt.find("div", {"class": "checkpoint-time"})

                description = status_div.text.strip() if status_div else ""
                location = location_div.text.strip() if location_div else ""

                date_txt = date_div.text.strip() if date_div else ""
                time_txt = time_div.text.strip() if time_div else ""

                full_date_str = f"{date_txt} {time_txt}"

                try:
                    if "," in full_date_str:
                        date_part = full_date_str.split(", ")[1]
                    else:
                        date_part = full_date_str

                    dt = datetime.strptime(date_part, "%d/%m/%Y %H:%M")
                except ValueError:
                    dt = datetime.now()

                package.locations.append(
                    Location(datetime=dt, location=location, description=description)
                )

            return package

        except Exception as e:
            logger.error(f"Error tracking Geniki package: {e}")
            return package

