import logging
import configparser
import os.path

from constants import GroupingLevel
from main_window import MainWindow


def load_configuration(filename: str = "config.ini") -> str:
    config = configparser.ConfigParser()
    if not os.path.exists(filename):
        config['DEFAULT'] = {'grouping_level': '1'}
        with open(filename, "w") as config_file:
            config.write(config_file)

    fn = config.read(filename)
    assert fn, f"{fn=}"
    grouping_level = config["DEFAULT"].get("grouping_level", "0")
    try:
        grouping_level = int(grouping_level)
        mapping = {
            1: GroupingLevel.YYYY.value,
            2: GroupingLevel.YYYYMM.value,
            3: GroupingLevel.YYYYMMDD.value,
        }
        return mapping[grouping_level]
    except (ValueError, KeyError):
        logging.warning(f"Please remove {filename} file (it will be restored to defaults).")
        return GroupingLevel.YYYY.value


def main():
    grouping_level: str = load_configuration()
    logging.info(f"{grouping_level=}")
    app = MainWindow(grouping_level)  # TODO: MainWindow doesn't care. OrganizePhotos should be initialized with this.
    app.mainloop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
