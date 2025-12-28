from abc import ABC, abstractmethod

from src.core.models import Package


class CourierTracker(ABC):
    """Abstract base class for all courier trackers."""

    @abstractmethod
    def track(self, tracking_number: str) -> Package:
        """
        Track a package by its tracking number.

        Args:
            tracking_number: The tracking number to look up

        Returns:
            Package object with tracking information
        """
        pass
