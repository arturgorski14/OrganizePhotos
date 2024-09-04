from unittest.mock import patch

from select_folder import select_folder


def test_select_folder_with_selection(caplog):
    # Mock the askdirectory method to return a specific folder path
    expected_folder_path = "/path/to/folder"
    with patch("tkinter.filedialog.askdirectory", return_value=expected_folder_path):
        folder_name = select_folder()

        # Assert the expected output
        assert folder_name == expected_folder_path
        assert "Selected folder: /path/to/folder" in caplog.text


def test_select_folder_without_selection(caplog):
    # Mock the askdirectory method to return an empty string (simulating no selection)
    expected_folder_path = ""
    with patch("tkinter.filedialog.askdirectory", return_value=expected_folder_path):
        folder_name = select_folder()

        # Assert the expected output
        assert folder_name == expected_folder_path
        assert "No folder selected" in caplog.text
