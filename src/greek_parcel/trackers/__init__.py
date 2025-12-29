from typing import Optional

from greek_parcel.trackers.base import CourierTracker
from greek_parcel.trackers.acs import ACSTracker
from greek_parcel.trackers.boxnow import BoxNowTracker
from greek_parcel.trackers.courier_center import CourierCenterTracker
from greek_parcel.trackers.easymail import EasyMailTracker
from greek_parcel.trackers.elta import EltaTracker
from greek_parcel.trackers.geniki import GenikiTracker
from greek_parcel.trackers.skroutz import SkroutzTracker
from greek_parcel.trackers.speedex import SpeedexTracker

_TRACKER_REGISTRY: dict[str, type[CourierTracker]] = {
    "acs": ACSTracker,
    "boxnow": BoxNowTracker,
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
    "BoxNowTracker",
    "CourierCenterTracker",
    "EasyMailTracker",
    "EltaTracker",
    "GenikiTracker",
    "SkroutzTracker",
    "SpeedexTracker",
    "get_tracker",
    "list_couriers",
]
