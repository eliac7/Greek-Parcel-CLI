"""Custom exception classes for package tracking."""

from typing import Optional


class TrackingError(Exception):
    """Base exception for all tracking-related errors."""

    pass


class CourierNotFoundError(TrackingError):
    """Raised when a courier name is not recognized."""

    def __init__(self, courier_name: str):
        self.courier_name = courier_name
        super().__init__(f"Unknown courier: {courier_name}")


class PackageNotFoundError(TrackingError):
    """Raised when a package cannot be found for the given tracking number."""

    def __init__(self, tracking_number: str, courier_name: str):
        self.tracking_number = tracking_number
        self.courier_name = courier_name
        super().__init__(
            f"Package {tracking_number} not found for courier {courier_name}"
        )


class NetworkError(TrackingError):
    """Raised when a network error occurs during tracking."""

    def __init__(self, message: str, original_error: Optional[Exception] = None):
        self.original_error = original_error
        super().__init__(f"Network error: {message}")

