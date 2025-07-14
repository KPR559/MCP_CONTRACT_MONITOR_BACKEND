from enum import Enum

class Location(str, Enum):
    """Enumeration of valid contract locations."""
    CHENNAI = "Chennai"
    MUMBAI = "Mumbai"
    BENGALURU = "Bengaluru"
    HYDERABAD = "Hyderabad"
