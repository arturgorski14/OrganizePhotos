import pytest

from group_files_by_date import GroupingLevel, group_files_by_date


@pytest.mark.parametrize(
    "files, grouping_level, expected",
    [
        (
            [
                "IMG_20230901_something.jpg",
                "VID_20240902_something.mp4",
                "IMG_20241001_something.jpg",
                "PANO_20241001_something.jpg",
            ],
            GroupingLevel.YYYY,
            {
                "2023": ["IMG_20230901_something.jpg"],
                "2024": ["VID_20240902_something.mp4", "IMG_20241001_something.jpg", "PANO_20241001_something.jpg"],
            },
        ),
        (
            [
                "IMG_20230901_something.jpg",
                "VID_20240902_something.mp4",
                "IMG_20241001_something.jpg",
                "PANO_20241001_something.jpg",
            ],
            GroupingLevel.YYYYMM,
            {
                "2023.09": ["IMG_20230901_something.jpg"],
                "2024.09": ["VID_20240902_something.mp4"],
                "2024.10": ["IMG_20241001_something.jpg", "PANO_20241001_something.jpg"],
            },
        ),
        (
            [
                "IMG_20230901_something.jpg",
                "VID_20240902_something.mp4",
                "IMG_20241001_something.jpg",
                "PANO_20241001_something.jpg",
            ],
            GroupingLevel.YYYYMMDD,
            {
                "2023.09.01": ["IMG_20230901_something.jpg"],
                "2024.09.02": ["VID_20240902_something.mp4"],
                "2024.10.01": ["IMG_20241001_something.jpg", "PANO_20241001_something.jpg"],
            },
        ),
    ],
)
def test_group_files_by_date(files, grouping_level, expected):
    grouped_files = group_files_by_date(files, grouping_level)
    assert grouped_files == expected
