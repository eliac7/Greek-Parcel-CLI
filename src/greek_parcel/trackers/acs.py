import logging
import re
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from greek_parcel.core.constants import DEFAULT_TIMEOUT
from greek_parcel.core.models import Location, Package
from greek_parcel.trackers.base import CourierTracker
from greek_parcel.utils.user_agents import get_random_user_agent

logger = logging.getLogger(__name__)


class ACSTracker(CourierTracker):

    def _get_encrypted_key(self) -> str | None:
        """
        Fetch the encrypted key from the ACS website.
        The key is stored in the publicToken attribute of the app-root element.

        Returns:
            The encrypted key if found, None otherwise
        """
        try:
            urls_to_try = [
                "https://www.acscourier.net/el/myacs/anafores-apostolwn/anazitisi-apostolwn/",
                "https://www.acscourier.net/track",
                "https://www.acscourier.net/",
            ]

            headers = {
                "user-agent": get_random_user_agent(),
                "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "accept-language": "el",
                "referer": "https://www.acscourier.net/",
            }

            for page_url in urls_to_try:
                try:
                    response = requests.get(
                        page_url, headers=headers, timeout=DEFAULT_TIMEOUT
                    )
                    if response.status_code != 200:
                        continue

                    html_content = response.text
                    soup = BeautifulSoup(html_content, "html.parser")

                    app_root = soup.find("div", {"id": "app-root"})
                    if app_root:
                        public_token = app_root.get("publictoken")
                        if public_token and len(public_token) > 50:
                            logger.debug(f"Found publicToken from {page_url}")
                            return public_token

                    pattern = r'publicToken=["\']([A-Za-z0-9_-]{100,})["\']'
                    match = re.search(pattern, html_content, re.IGNORECASE)
                    if match:
                        key = match.group(1)
                        if len(key) > 50:
                            logger.debug(f"Found publicToken via regex from {page_url}")
                            return key

                except Exception as e:
                    logger.debug(f"Error fetching {page_url}: {e}")
                    continue

            logger.warning("Could not find encrypted key on ACS website")
            return None

        except Exception as e:
            logger.error(f"Error fetching encrypted key: {e}")
            return None

    def track(self, tracking_number: str) -> Package:
        """Track an ACS package."""
        package = Package(courier_name="ACS")
        url = f"https://api.acscourier.net/api/parcels/search/{tracking_number}"

        try:
            encrypted_key = self._get_encrypted_key()
            if not encrypted_key:
                logger.error("Could not fetch encrypted key from ACS website")
                return package

            headers = {
                "accept": "application/json",
                "accept-language": "el",
                "authorization": "Bearer null",
                "dnt": "1",
                "origin": "https://www.acscourier.net",
                "priority": "u=1, i",
                "referer": "https://www.acscourier.net/",
                "sec-ch-ua": '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"Windows"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "user-agent": get_random_user_agent(),
                "x-country": "GR",
                "x-encrypted-key": encrypted_key,
                "x-subscription-id": "",
            }
            response = requests.get(url, headers=headers, timeout=DEFAULT_TIMEOUT)

            if response.status_code != 200:
                # 400/404 is expected if the tracking number is invalid for ACS
                if response.status_code in [400, 404]:
                     logger.debug(f"ACS returned status code {response.status_code} (likely invalid number for ACS)")
                else:
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
