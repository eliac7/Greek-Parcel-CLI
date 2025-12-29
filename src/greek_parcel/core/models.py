from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class Location:
    datetime: datetime
    location: str
    description: str


@dataclass
class Package:
    found: bool = False
    courier_name: str = ""
    locations: List[Location] = field(default_factory=list)
    delivered: bool = False
