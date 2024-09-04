import os
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def get_matching_files(folder_path):
    if not folder_path:
        return []

    # Regular expression patterns for the file formats
    patterns = [
        r"^IMG_\d{8}_.*\.jpg$",  # Matches IMG_YYYYMMDD_*.jpg
        r"^VID_\d{8}_.*\.mp4$",  # Matches VID_YYYYMMDD_*.mp4
        r"^PANO_\d{8}_.*\.jpg$",  # Matches PANO_YYYYMMDD_*.jpg
    ]

    matching_files = []

    # Iterate over all files in the selected folder
    for filename in os.listdir(folder_path):
        # Check if the filename matches any of the patterns
        if any(re.match(pattern, filename) for pattern in patterns):
            matching_files.append(filename)

    logging.info(f"Found {len(matching_files)} matching files")

    return matching_files
