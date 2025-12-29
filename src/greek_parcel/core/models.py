from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class Location:
    datetime: datetime
    location: str
    description: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "datetime": self.datetime.isoformat(),
            "location": self.location,
            "description": self.description,
        }


@dataclass
class Package:
    found: bool = False
    courier_name: str = ""
    locations: List[Location] = field(default_factory=list)
    delivered: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "found": self.found,
            "courier_name": self.courier_name,
            "delivered": self.delivered,
            "locations": [loc.to_dict() for loc in self.locations],
        }
