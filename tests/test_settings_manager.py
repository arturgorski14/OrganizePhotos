import configparser
from unittest import mock

import pytest

from constants import GroupingLevel
from settings_manager import SettingsManager


@pytest.fixture
def config():
    return configparser.ConfigParser()


@pytest.fixture
def settings_manager(config):
    return SettingsManager(config)


def test_read_settings_creates_default_file(settings_manager, tmp_path):
    # Arrange: Set up a temporary filename and mock the existence check
    temp_file = tmp_path / "temp_settings.ini"

    # Act: Read settings should create the file with default settings
    settings_manager._read_settings(temp_file)

    # Assert: Check that the file has been created and contains the default settings
    assert temp_file.exists()
    assert (
        settings_manager.config[SettingsManager.SECTION][SettingsManager.GROUPING_LEVEL]
        == "1"
    )


def test_get_grouping_level_returns_default(settings_manager, tmp_path):
    temp_file = tmp_path / "temp_settings.ini"

    # Act: Call get_grouping_level which should create the default file and return the default grouping level
    result = settings_manager.get_grouping_level(temp_file)

    # Assert: Ensure the result matches the default grouping level
    assert result == GroupingLevel.YYYY.value


def test_get_grouping_level_handles_invalid_value(settings_manager, tmp_path):
    temp_file = tmp_path / "temp_settings.ini"

    # Arrange: Manually create a config file with an invalid grouping level
    settings_manager.config[SettingsManager.SECTION] = {
        SettingsManager.GROUPING_LEVEL: "invalid"
    }
    with open(temp_file, "w") as config_file:
        settings_manager.config.write(config_file)

    # Act: Call get_grouping_level which should handle the invalid value
    result = settings_manager.get_grouping_level(temp_file)

    # Assert: Ensure it returns the default grouping level when the value is invalid
    assert result == GroupingLevel.YYYY.value


@mock.patch("os.path.exists", return_value=True)
def test_set_grouping_level_updates_file(mock_exists, settings_manager, tmp_path):
    temp_file = tmp_path / "temp_settings.ini"

    # Act: Set a new grouping level
    settings_manager.set_grouping_level(GroupingLevel.YYYYMM, temp_file)

    # Assert: Check if the file is updated with the new grouping level
    settings_manager.config.read(temp_file)
    assert (
        settings_manager.config[SettingsManager.SECTION][SettingsManager.GROUPING_LEVEL]
        == "2"
    )


@mock.patch("os.path.exists", return_value=False)
def test_read_settings_creates_new_config_file(mock_exists, settings_manager, tmp_path):
    temp_file = tmp_path / "temp_settings.ini"

    # Act: Read settings should create the file since it doesn't exist
    settings_manager._read_settings(temp_file)

    # Assert: Check if the config is created with default grouping level
    assert (
        settings_manager.config[SettingsManager.SECTION][SettingsManager.GROUPING_LEVEL]
        == "1"
    )
    assert temp_file.exists()


@mock.patch("logging.warning")
def test_get_grouping_level_logs_warning_on_invalid_grouping_level(
    mock_warning, settings_manager, tmp_path
):
    temp_file = tmp_path / "temp_settings.ini"

    # Arrange: Create a config file with an invalid grouping level
    settings_manager.config[SettingsManager.SECTION] = {
        SettingsManager.GROUPING_LEVEL: "4"
    }
    with open(temp_file, "w") as config_file:
        settings_manager.config.write(config_file)

    # Act: Call get_grouping_level which should log a warning
    settings_manager.get_grouping_level(temp_file)

    # Assert: Ensure the warning was logged
    mock_warning.assert_called_once_with(
        f"Please remove {temp_file} file (it will be restored to defaults)."
    )
