import json
from pathlib import Path
from typing import Dict, List, Optional

HISTORY_FILE = Path.home() / ".greek_parcel_history.json"


def load_history() -> List[Dict]:
    """Load tracking history from the local JSON file."""
    if not HISTORY_FILE.exists():
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_history(history: List[Dict]):
    """Save tracking history to the local JSON file."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4, ensure_ascii=False)
    except IOError:
        pass


def is_in_history(tracking_number: str) -> bool:
    """Check if a tracking number is already saved."""
    history = load_history()
    return any(item["tracking_number"] == tracking_number for item in history)


def add_to_history(tracking_number: str, courier: str, alias: Optional[str] = None):
    """Add or update a tracking number in the history."""
    history = load_history()

    # Check if already exists
    for item in history:
        if item["tracking_number"] == tracking_number:
            if alias is not None:
                item["alias"] = alias
            item["courier"] = courier
            save_history(history)
            return

    # Add new item
    history.append(
        {
            "tracking_number": tracking_number,
            "courier": courier,
            "alias": alias or "",
        }
    )
    save_history(history)


def remove_from_history(tracking_number: str):
    """Remove a tracking number from the history."""
    history = load_history()
    new_history = [
        item for item in history if item["tracking_number"] != tracking_number
    ]
    save_history(new_history)


def update_alias(tracking_number: str, alias: str):
    """Update the alias for a tracking number."""
    history = load_history()
    for item in history:
        if item["tracking_number"] == tracking_number:
            item["alias"] = alias
            save_history(history)
            return True
    return False
