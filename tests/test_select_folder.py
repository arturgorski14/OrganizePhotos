import logging
from unittest.mock import patch

from select_folder import select_folder


def test_select_folder_with_selection(caplog):
    expected_folder_path = "/path/to/folder"
    with patch(
        "select_folder.filedialog.askdirectory", return_value=expected_folder_path
    ):
        with caplog.at_level(logging.INFO):
            folder_name = select_folder()

        assert folder_name == expected_folder_path
        assert "Selected folder: /path/to/folder" in caplog.text


def test_select_folder_without_selection(caplog):
    expected_folder_path = ""
    with patch(
        "select_folder.filedialog.askdirectory", return_value=expected_folder_path
    ):
        with caplog.at_level(logging.INFO):
            folder_name = select_folder()

    assert folder_name == expected_folder_path
    assert "No folder selected" in caplog.text
