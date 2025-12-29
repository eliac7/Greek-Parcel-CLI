import logging
from datetime import datetime

import requests

from greek_parcel.core.constants import DEFAULT_TIMEOUT, DEFAULT_USER_AGENT
from greek_parcel.core.models import Location, Package
from greek_parcel.trackers.base import CourierTracker

logger = logging.getLogger(__name__)


class BoxNowTracker(CourierTracker):
    def track(self, tracking_number: str) -> Package:
        """Track a BoxNow package."""
        package = Package(courier_name="BoxNow")
        url = "https://api-production.boxnow.gr/api/v1/parcels:track"

        try:
            headers = {
                "accept": "application/json, text/javascript, */*; q=0.01",
                "accept-language": "en-US,en;q=0.9,el;q=0.8,de;q=0.7",
                "content-type": "application/json",
                "dnt": "1",
                "origin": "https://boxnow.gr",
                "priority": "u=1, i",
                "referer": "https://boxnow.gr/",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "user-agent": DEFAULT_USER_AGENT,
            }

            response = requests.post(
                url,
                json={"parcelId": tracking_number},
                headers=headers,
                timeout=DEFAULT_TIMEOUT,
            )
            response.raise_for_status()
            data = response.json()

            # Check if package was found
            if not data or not isinstance(data, dict):
                return package

            parcels = data.get("data", [])
            if not parcels or not isinstance(parcels, list):
                return package

            # Get the first parcel (usually there's only one)
            parcel = parcels[0] if parcels else {}
            if not isinstance(parcel, dict):
                return package

            package.found = True

            # Check delivery status from parcel state
            if parcel.get("state") == "delivered":
                package.delivered = True

            # Get events from the parcel
            events = parcel.get("events", [])
            if not isinstance(events, list):
                return package

            for event in events:
                if not isinstance(event, dict):
                    continue

                dt = datetime.now()
                create_time = event.get("createTime")
                if create_time:
                    try:
                        # Parse ISO format: "2025-11-18T13:55:32.015Z"
                        dt = datetime.fromisoformat(create_time.replace("Z", "+00:00"))
                    except (ValueError, AttributeError):
                        pass

                location = event.get("locationDisplayName", "")

                event_type = event.get("type", "")

                type_mapping = {
                    "new": "Νέα παραγγελία",
                    "in-depot": "Σε αποθήκη",
                    "final-destination": "Στο τελικό σημείο",
                    "delivered": "Παραδόθηκε",
                }
                description = type_mapping.get(event_type, event_type)

                package.locations.append(
                    Location(datetime=dt, location=location, description=description)
                )

            package.locations.sort(key=lambda x: x.datetime)

            return package

        except Exception as e:
            logger.error(f"Error tracking BoxNow package: {e}")
            return package
