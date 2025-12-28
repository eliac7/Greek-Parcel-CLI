import logging
import re
from datetime import datetime

import requests

from src.core.constants import DEFAULT_TIMEOUT, DELIVERY_INDICATORS, DEFAULT_USER_AGENT
from src.core.models import Location, Package
from src.trackers.base import CourierTracker

logger = logging.getLogger(__name__)

_TIME_HH_MM = re.compile(r"^\s*(\d{1,2})\s*:\s*(\d{1,2})\s*$")
_TIME_HH_COLON = re.compile(r"^\s*(\d{1,2})\s*:\s*$")


def _safe_elta_datetime(date_part: str, time_part: str) -> datetime:
    try:
        d = datetime.strptime((date_part or "").strip(), "%d-%m-%Y").date()
    except ValueError:
        return datetime(1970, 1, 1, 0, 0)

    t = (time_part or "").strip()
    m = _TIME_HH_MM.match(t)
    if m:
        hh, mm = int(m.group(1)), int(m.group(2))
        if 0 <= hh <= 23 and 0 <= mm <= 59:
            return datetime(d.year, d.month, d.day, hh, mm)

    m = _TIME_HH_COLON.match(t)
    if m:
        hh = int(m.group(1))
        if 0 <= hh <= 23:
            return datetime(d.year, d.month, d.day, hh, 0)

    return datetime(d.year, d.month, d.day, 0, 0)


class EltaTracker(CourierTracker):
    def track(self, tracking_number: str) -> Package:
        package = Package(courier_name="ELTA")
        url = "https://www.elta-courier.gr/track.php"

        try:
            response = requests.post(
                url,
                data={"number": tracking_number},
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "User-Agent": DEFAULT_USER_AGENT,
                },
                timeout=DEFAULT_TIMEOUT,
            )
            response.raise_for_status()
            response.encoding = "utf-8-sig"
            data = response.json()

            result = data.get("result") or {}
            if tracking_number not in result:
                return package

            package_data = result[tracking_number]
            if package_data.get("status") == 0:
                return package

            package.found = True
            history = package_data.get("result") or []
            locations: list[Location] = []

            for item in history:
                dt = _safe_elta_datetime(item.get("date", ""), item.get("time", ""))
                locations.append(
                    Location(
                        datetime=dt,
                        location=item.get("place", "") or "",
                        description=item.get("status", "") or "",
                    )
                )

            locations.sort(key=lambda x: x.datetime)
            package.locations.extend(locations)

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
