import logging
from typing import List

import pytest

from grouping_level import GroupingLevel
from organize_photos import OrganizePhotos


class TestGetMatchingFiles:
    @pytest.fixture
    def setup_app(self, tmp_path):
        # Create an instance of OrganizePhotos with dummy folder_path and grouping level
        app = OrganizePhotos(str(tmp_path), grouping_level=GroupingLevel.YYYY)
        return app

    @pytest.mark.parametrize(
        "test_files, expected_matches",
        [
            (
                [  # REDMI
                    "IMG_20230901_something.jpg",
                    "VID_20230902_anotherthing.mp4",
                    "PANO_20230903_yetanotherthing.jpg",
                ],
                [
                    "IMG_20230901_something.jpg",
                    "VID_20230902_anotherthing.mp4",
                    "PANO_20230903_yetanotherthing.jpg",
                ],
            ),
            (
                # SAMSUNG
                ["20240721_161757.jpg", "20240925_211300.mp4"],
                ["20240721_161757.jpg", "20240925_211300.mp4"],
            ),
            (
                # Whatsapp
                ["IMG-20241005-WA0001.jpg", "VID-20241005-WA0014.mp4"],
                ["IMG-20241005-WA0001.jpg", "VID-20241005-WA0014.mp4"],
            ),
            (
                [
                    "NOT_A_MATCH_20230903.txt",
                    "unsupported_type_20230903.png",
                    "random_file.jpg",
                    "VID_20230902_impostor.txt",
                    "IMG_20230901_impostor.png",
                    "20240925_211300.png",
                ],
                [],
            ),
            ([], []),
        ],
    )
    def test_get_matching_files_with_matches(
        self, tmpdir, setup_app, caplog, test_files, expected_matches
    ):
        app = setup_app
        self.__populate_folder(tmpdir, test_files)

        with caplog.at_level(logging.INFO):
            matching_files = app.get_matching_files(str(tmpdir))

        assert sorted(matching_files) == sorted(expected_matches)
        self.__assert_log_message(caplog, matching_files, test_files)

    def __populate_folder(self, directory, filenames: List[str]) -> None:
        for filename in filenames:
            directory.join(filename).write("test content")

    def __assert_log_message(
        self, caplog, matched_files: List[str], all_files: List[str]
    ) -> bool:
        assert (
            f"Found {len(matched_files)} matching files out of {len(all_files)}"
            in caplog.text
        )
        return True
