import configparser
import logging

from main_window import MainWindow
from settings_manager import SettingsManager


def main():
    settings_manager = SettingsManager(configparser.ConfigParser())
    app = MainWindow(
        settings_manager
    )  # TODO: MainWindow doesn't care. OrganizePhotos should be initialized with this.
    app.mainloop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
