from typing import Optional

from src.trackers.base import CourierTracker
from src.trackers.acs import ACSTracker
from src.trackers.courier_center import CourierCenterTracker
from src.trackers.easymail import EasyMailTracker
from src.trackers.elta import EltaTracker
from src.trackers.geniki import GenikiTracker
from src.trackers.skroutz import SkroutzTracker
from src.trackers.speedex import SpeedexTracker

_TRACKER_REGISTRY: dict[str, type[CourierTracker]] = {
    "acs": ACSTracker,
    "couriercenter": CourierCenterTracker,
    "easymail": EasyMailTracker,
    "elta": EltaTracker,
    "geniki": GenikiTracker,
    "skroutz": SkroutzTracker,
    "speedex": SpeedexTracker,
}


def get_tracker(courier_name: str) -> Optional[CourierTracker]:
    """
    Get a tracker instance for the given courier name.

    Args:
        courier_name: Name of the courier (case-insensitive)

    Returns:
        Tracker instance or None if courier not found
    """
    name = courier_name.lower()
    tracker_class = _TRACKER_REGISTRY.get(name)
    if tracker_class:
        return tracker_class()
    return None


def list_couriers() -> list[str]:
    """
    Get a list of all supported courier names.

    Returns:
        List of courier names
    """
    return list(_TRACKER_REGISTRY.keys())


__all__ = [
    "CourierTracker",
    "ACSTracker",
    "CourierCenterTracker",
    "EasyMailTracker",
    "EltaTracker",
    "GenikiTracker",
    "SkroutzTracker",
    "SpeedexTracker",
    "get_tracker",
    "list_couriers",
]
