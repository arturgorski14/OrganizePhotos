from enum import Enum

DEFAULT_BUTTON_COLOR = "#f0f0f0"
ACTIVE_BUTTON_COLOR = "#74B72E"
USER_ACTION_NEEDED_COLOR = "yellow"


# Regular expression patterns for the file formats
PATTERNS = [
    r"^IMG.\d{8}..*\.jpg$",  # Matches IMG<any>YYYYMMDD<any>*.jpg
    r"^\d{8}_.*\.jpg$",  # Matches YYYYMMDD_*.jpg
    r"^VID.\d{8}..*\.mp4$",  # Matches VID<any>YYYYMMDD<any>*.mp4
    r"^\d{8}_.*\.mp4$",  # Matches YYYYMMDD_*.mp4
    r"^PANO.\d{8}..*\.jpg$",  # Matches PANO<any>YYYYMMDD<any>*.jpg
]


class ButtonState(Enum):
    active = "active"
    normal = "normal"
    disabled = "disabled"


class GroupingLevel(Enum):
    YYYY = "Po roku"
    YYYYMM = "Po roku i miesiącu"
    YYYYMMDD = "Po roku, miesiącu i dniu"
