from collections import defaultdict
from enum import Enum
from typing import Dict, List


class GroupingLevel(Enum):
    YYYY = 1
    YYYYMM = 2
    YYYYMMDD = 3


def _extract_date_part(filename: str, grouping: GroupingLevel) -> str:
    """
    Extracts the date part from the filename based on the grouping level.

    Parameters:
    - filename: The name of the file.
    - grouping: The level of grouping (GroupingLevel).

    Returns:
    - The extracted date part as a string.
    """
    # Extract the date part from the filename
    # Assuming filenames are in the format: PREFIX_YYYYMMDD_rest.ext
    parts = filename.split("_")
    date_part = parts[1]  # YYYYMMDD

    year = date_part[:4]
    month = date_part[4:6]
    day = date_part[6:8]

    if grouping == GroupingLevel.YYYY:
        return year
    elif grouping == GroupingLevel.YYYYMM:
        return f"{year}.{month}"
    elif grouping == GroupingLevel.YYYYMMDD:
        return f"{year}.{month}.{day}"


def group_files_by_date(
    file_list: List[str], grouping: GroupingLevel
) -> Dict[str, List[str]]:
    """
    Groups files by date based on the filename and the specified grouping level.

    Parameters:
    - file_list: List of filenames to be grouped.
    - grouping: The level of grouping (GroupingLevel).

    Returns:
    - A dictionary where the keys are the date groups and the values are lists of filenames in each group.
    """
    grouped_files = defaultdict(list)

    for filename in file_list:
        date_part = _extract_date_part(filename, grouping)
        if date_part:
            grouped_files[date_part].append(filename)

    return dict(grouped_files)
