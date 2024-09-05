import logging

from get_matching_files import get_matching_files


def test_get_matching_files_with_matches(tmpdir, caplog):
    # Create a temporary directory with some test files
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
        matching_files = get_matching_files(str(tmpdir))

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


def test_get_matching_files_without_matches(tmpdir, caplog):
    # Create a temporary directory with files that don't match the pattern
    test_files = ["VID_20230902_impostor.txt", "IMG_20230901_impostor.png"]

    for filename in test_files:
        tmpdir.join(filename).write("test content")

    with caplog.at_level(logging.INFO):
        matching_files = get_matching_files(str(tmpdir))

    # Assert that the result is an empty list
    assert matching_files == []

    # Assert that the log contains the correct message
    assert "Found 0 matching files" in caplog.text


def test_get_matching_files_empty_folder(tmpdir, caplog):
    # Ensure the directory is empty
    with caplog.at_level(logging.INFO):
        matching_files = get_matching_files(str(tmpdir))

    # Assert that the result is an empty list
    assert matching_files == []

    # Assert that the log contains the correct message
    assert "Found 0 matching files" in caplog.text
