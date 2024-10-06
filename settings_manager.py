import configparser
import logging
import os
from pathlib import Path

from constants import GroupingLevel


class SettingsManager:
    DEFAULT_FILENAME = "settings.ini"
    SECTION = "LAST_USED"
    GROUPING_LEVEL = "grouping_level"

    def __init__(self, config: configparser.ConfigParser):
        self.config = config

    def get_grouping_level(self, filename: str | Path = DEFAULT_FILENAME) -> str:
        self._read_settings(filename)
        grouping_level = self.config[self.SECTION].get(self.GROUPING_LEVEL, "0")
        try:
            grouping_level = int(grouping_level)
            mapping = {
                1: GroupingLevel.YYYY.value,
                2: GroupingLevel.YYYYMM.value,
                3: GroupingLevel.YYYYMMDD.value,
            }
            return mapping[grouping_level]
        except (ValueError, KeyError):
            logging.warning(
                f"Please remove {filename} file (it will be restored to defaults)."
            )
            return GroupingLevel.YYYY.value

    def set_grouping_level(
        self, grouping_level: GroupingLevel, filename: str | Path = DEFAULT_FILENAME
    ):
        mapping = {
            GroupingLevel.YYYY: "1",
            GroupingLevel.YYYYMM: "2",
            GroupingLevel.YYYYMMDD: "3",
        }
        mapped_grouping_level = mapping[grouping_level]
        self.config[self.SECTION] = {self.GROUPING_LEVEL: mapped_grouping_level}
        with open(filename, "w") as config_file:
            self.config.write(config_file)

    def _read_settings(self, filename: str | Path = DEFAULT_FILENAME) -> None:
        if not os.path.exists(filename):
            self.config[self.SECTION] = {self.GROUPING_LEVEL: "1"}
            with open(filename, "w") as config_file:
                self.config.write(config_file)
        self.config.read(filename)
