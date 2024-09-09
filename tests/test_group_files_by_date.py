from unittest.mock import MagicMock

import pytest

from grouping_level import GroupingLevel
from organize_photos import OrganizePhotos


class TestGroupFilesByDate:
    @pytest.fixture
    def setup_app(self, tmp_path):
        # Create an instance of OrganizePhotos with dummy folder_path and grouping level
        app = OrganizePhotos(str(tmp_path), grouping_level=GroupingLevel.YYYY)

        # Mock GUI components
        app.progress_bar = MagicMock()
        app.progress_bar_label = MagicMock()
        return app

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
                    "2024": [
                        "VID_20240902_something.mp4",
                        "IMG_20241001_something.jpg",
                        "PANO_20241001_something.jpg",
                    ],
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
                    "2024.10": [
                        "IMG_20241001_something.jpg",
                        "PANO_20241001_something.jpg",
                    ],
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
                    "2024.10.01": [
                        "IMG_20241001_something.jpg",
                        "PANO_20241001_something.jpg",
                    ],
                },
            ),
        ],
    )
    def test_group_files_by_date(self, files, setup_app, grouping_level, expected):
        app = setup_app

        grouped_files = app.group_files_by_date(files, grouping_level)

        assert grouped_files == expected
