import re
from typing import List

# Courier Regex Patterns
# Sources:
# - ACS: 10 digits
# - Geniki: 10 digits usually (sometimes alphanumeric)
# - BoxNow: 10 digits
# - Speedex: SP + 8-10 digits, or 12 digits, or 9 digits + 2 letters
# - ELTA: Standard UPU (XX123456789XX) or 12 digits
# - Skroutz: 13 chars alphanumeric
# - EasyMail: Often standard UPU or similar
# - CourierCenter: 12 digits (often)

COURIER_PATTERNS = {
    "acs": [r"^\d{10}$"],
    "geniki": [r"^\d{10}$", r"^[A-Z0-9]{8,40}$"],
    "boxnow": [r"^\d{10}$"],
    "speedex": [
        r"^SP\d{8,10}$",  # SP1234567890
        r"^\d{12}$",  # 12 digits
        r"^\d{9}[A-Z]{2}$",  # 9 digits + 2 letters
        r"^[A-Z]{2,5}\d{6,10}$",  # Generic prefix + digits
    ],
    "elta": [r"^[A-Z]{2}\d{9}[A-Z]{2}$", r"^\d{12}$"],  # Standard UPU  # 12 digits
    "skroutz": [r"^[A-Z0-9]{13}$"],
    "easymail": [r"^EM\d{9}[A-Z]{2}$", r"^\d{11}$", r"^\d{10,12}$"],
    "couriercenter": [r"^\d{12}$", r"^\d{10,12}$"],
}


def identify_courier(tracking_number: str) -> List[str]:
    """
    Identify potential couriers based on tracking number format.

    Args:
        tracking_number: The tracking number to analyze.

    Returns:
        List of courier names that match the pattern.
    """
    candidates = []

    cleaned_number = tracking_number.strip().upper()

    for courier, patterns in COURIER_PATTERNS.items():
        for pattern in patterns:
            try:
                if re.match(pattern, cleaned_number):
                    candidates.append(courier)
                    break  # Match found for this courier, move to next courier
            except re.error:
                continue

    return candidates
