from enum import Enum

class Status(str, Enum):
    """Enumeration of contract status values."""
    ACTIVE = "active"
    INACTIVE = "inactive"