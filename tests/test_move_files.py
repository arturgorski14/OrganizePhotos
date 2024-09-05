from pathlib import Path

import pytest

from move_files import move_files


@pytest.fixture
def setup_files(tmp_path):
    """
    Set up a temporary file structure for testing.
    """
    files = [tmp_path / "file1.txt", tmp_path / "file2.txt", tmp_path / "file3.txt"]

    # Create files in the temporary directory
    for file in files:
        file.touch()

    # Simulated grouped files structure
    grouped_files = {
        "group1": [str(files[0]), str(files[1])],
        "group2": [str(files[2])],
    }

    return grouped_files, tmp_path


def test_move_files(setup_files):
    grouped_files, tmp_path = setup_files

    # Destination folder for the test
    destination_folder = tmp_path / "destination"
    destination_folder.mkdir()

    # Call the move_files function
    move_files(grouped_files, destination_folder)

    # Verify that the files were moved to the correct locations
    for group, files in grouped_files.items():
        target_folder = destination_folder / group
        for file_path in files:
            assert (
                target_folder / Path(file_path).name
            ).exists(), f"{file_path} not found in {target_folder}"

    # Ensure original files are not in the source folder anymore
    for files in grouped_files.values():
        for file_path in files:
            assert not Path(
                file_path
            ).exists(), f"{file_path} still exists in the original location"
