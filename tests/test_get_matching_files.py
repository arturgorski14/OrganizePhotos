import logging

import pytest

from grouping_level import GroupingLevel
from organize_photos import OrganizePhotos


class TestGetMatchingFiles:
    @pytest.fixture
    def setup_app(self, tmp_path):
        # Create an instance of OrganizePhotos with dummy folder_path and grouping level
        app = OrganizePhotos(str(tmp_path), grouping_level=GroupingLevel.YYYY)
        return app

    def test_get_matching_files_with_matches(self, tmpdir, setup_app, caplog):
        # Create a temporary directory with some test files
        app = setup_app
        test_files = [
            "IMG_20230901_something.jpg",
            "VID_20230902_anotherthing.mp4",
            "PANO_20230903_yetanotherthing.jpg",
            "NOT_A_MATCH.txt",
            "random_file.png",
        ]

        for filename in test_files:
            tmpdir.join(filename).write("test content")

        with caplog.at_level(logging.INFO):
            matching_files = app.get_matching_files(str(tmpdir))

        # Assert that only the matching files are returned
        assert sorted(matching_files) == sorted(
            [
                "IMG_20230901_something.jpg",
                "VID_20230902_anotherthing.mp4",
                "PANO_20230903_yetanotherthing.jpg",
            ]
        )

        # Assert that the log contains the correct message
        assert "Found 3 matching files" in caplog.text

    def test_get_matching_files_without_matches(self, tmpdir, setup_app, caplog):
        app = setup_app
        # Create a temporary directory with files that don't match the pattern
        test_files = ["VID_20230902_impostor.txt", "IMG_20230901_impostor.png"]

        for filename in test_files:
            tmpdir.join(filename).write("test content")

        with caplog.at_level(logging.INFO):
            matching_files = app.get_matching_files(str(tmpdir))

        # Assert that the result is an empty list
        assert matching_files == []

        # Assert that the log contains the correct message
        assert "Found 0 matching files" in caplog.text

    def test_get_matching_files_empty_folder(self, tmpdir, setup_app, caplog):
        app = setup_app
        # Ensure the directory is empty
        with caplog.at_level(logging.INFO):
            matching_files = app.get_matching_files(str(tmpdir))

        # Assert that the result is an empty list
        assert matching_files == []

        # Assert that the log contains the correct message
        assert "Found 0 matching files" in caplog.text
