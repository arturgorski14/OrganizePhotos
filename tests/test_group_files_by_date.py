import pytest

from grouping_level import GroupingLevel
from organize_photos import OrganizePhotos


class TestGroupFilesByDate:
    @pytest.fixture
    def setup_app(self, tmp_path):
        # Create an instance of OrganizePhotos with dummy folder_path and grouping level
        app = OrganizePhotos(str(tmp_path), grouping_level=GroupingLevel.YYYY)
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
                    # REDMI
                    "IMG_20230901_something.jpg",
                    "VID_20240902_something.mp4",
                    "IMG_20241001_something.jpg",
                    "PANO_20241001_something.jpg",
                    # SAMSUNG
                    "20240721_161757.jpg",
                    "20240925_211300.mp4",
                    # Whatsapp
                    "IMG-20241005-WA0001.jpg",
                    "VID-20241005-WA0014.mp4",
                ],
                GroupingLevel.YYYYMMDD,
                {
                    "2023.09.01": ["IMG_20230901_something.jpg"],
                    "2024.07.21": ["20240721_161757.jpg"],
                    "2024.09.02": ["VID_20240902_something.mp4"],
                    "2024.09.25": ["20240925_211300.mp4"],
                    "2024.10.01": [
                        "IMG_20241001_something.jpg",
                        "PANO_20241001_something.jpg",
                    ],
                    "2024.10.05": [
                        "IMG-20241005-WA0001.jpg",
                        "VID-20241005-WA0014.mp4",
                    ],
                },
            ),
        ],
    )
    def test_group_files_by_date(self, files, setup_app, grouping_level, expected):
        app = setup_app

        grouped_files = app.group_files_by_date(files, grouping_level)

        assert grouped_files == expected
