import logging
import os
import re
import shutil
import tkinter as tk
from collections import defaultdict
from enum import Enum
from pathlib import Path
from tkinter import messagebox, ttk
from typing import Dict, List, Tuple
from unittest.mock import MagicMock

from grouping_level import GroupingLevel
from select_folder import select_folder


class ButtonState(Enum):
    active = "active"
    normal = "normal"
    disabled = "disabled"


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Organizer zdjęć")
        self.geometry("300x300")

        # initialize variables
        self.grouping_var = tk.IntVar(value=1)  # Default to GroupingLevel.YYYY

        # initialize widgets
        self.folder_label = tk.Label(self, text="Brak wybranego folderu")
        self.folder_btn = tk.Button(
            self, text="Wybierz folder!", command=self.select_folder
        )
        radio_btn1 = tk.Radiobutton(
            self, text="Po roku", variable=self.grouping_var, value=1
        )
        radio_btn2 = tk.Radiobutton(
            self, text="Po roku i miesiącu", variable=self.grouping_var, value=2
        )
        radio_btn3 = tk.Radiobutton(
            self, text="Po roku, miesiącu i dniu", variable=self.grouping_var, value=3
        )
        self.run_button = tk.Button(
            self,
            text="Uruchom!",
            command=self.create_new_window_and_organize,
            state="disabled",
        )

        # placement on the grid
        self.folder_label.pack()
        self.folder_btn.pack()
        radio_btn1.pack()
        radio_btn2.pack()
        radio_btn3.pack()
        self.run_button.pack()

    def select_folder(self) -> None:
        folder_path = select_folder()
        if not folder_path:
            self.folder_label["text"] = "Brak wybranego folderu"
            self.folder_btn["text"] = "Wybierz folder!"
            self.__change_button_state(self.run_button, ButtonState.disabled)
            return
        self.folder_label["text"] = folder_path
        self.folder_btn["text"] = "Wybrany folder:"
        self.__change_button_state(self.run_button, ButtonState.normal)

    def __change_button_state(
        self, button: tk.Button, desired_state: ButtonState
    ) -> None:
        button["state"] = desired_state.value

    def get_grouping_text(self):
        # Map the IntVar values to their corresponding text
        value = self.grouping_var.get()
        if value == 1:
            return "Po roku"
        elif value == 2:
            return "Po roku i miesiącu"
        elif value == 3:
            return "Po roku, miesiącu i dniu"
        else:
            return "Nieznany poziom"

    def get_grouping_level(self) -> GroupingLevel:
        value = self.grouping_var.get()
        if value == 1:
            return GroupingLevel.YYYY
        elif value == 2:
            return GroupingLevel.YYYYMM
        elif value == 3:
            return GroupingLevel.YYYYMMDD
        raise ValueError(f"Niepoprawny wybór {value=}")

    def create_new_window_and_organize(self) -> None:
        self.__change_button_state(self.run_button, ButtonState.disabled)
        self.__change_button_state(self.folder_btn, ButtonState.disabled)

        # progress_bar_label = tk.Label(self, text="Rozpoczynam.")
        files_length = len(os.listdir(self.folder_label["text"]))
        # progress_bar = ttk.Progressbar(orient=tk.HORIZONTAL, length=files_length * 3 + 1)
        # progress_bar_label.pack()
        # progress_bar.pack()

        command = OrganizePhotos(
            self.folder_label["text"],
            self.get_grouping_level(),
            files_length * 3,
            progress_bar=MagicMock(),
            progress_bar_label=MagicMock(),
        )
        command.organize()

        self.__change_button_state(self.run_button, ButtonState.normal)
        self.__change_button_state(self.folder_btn, ButtonState.normal)


class OrganizePhotos:

    def __init__(
        self,
        folder_path: str,
        grouping_level: GroupingLevel,
        number_of_steps: int = 1,
        progress_bar: ttk.Progressbar = MagicMock(),
        progress_bar_label: tk.Label = MagicMock(),
    ):
        self.folder_path = folder_path
        self.grouping_level = grouping_level
        self.step_increment = 1 / number_of_steps
        self.progress_bar = progress_bar
        self.progress_bar_label = progress_bar_label

    def organize(self) -> None:
        folder_path = self.folder_path
        grouping_level = self.grouping_level

        files = self.get_matching_files(folder_path)
        self.__update_label(f"{len(files)} plików może zostać przeniesionych.")
        grouped_files = self.group_files_by_date(files, grouping_level)
        self.__update_label(
            f"Liczba nowych folderów: {len(grouped_files)}\nI ich nazwy: {grouped_files.keys()}"
        )

        successes, failures = self.move_files(grouped_files, Path(folder_path))
        self.__update_label(f"Przeniesiono {successes} z {successes + failures} plików")

        self.__display_message_box(successes, failures)

    def get_matching_files(self, folder_path) -> List[str]:
        if not folder_path:
            return []

        # Regular expression patterns for the file formats
        patterns = [
            r"^IMG_\d{8}_.*\.jpg$",  # Matches IMG_YYYYMMDD_*.jpg
            r"^VID_\d{8}_.*\.mp4$",  # Matches VID_YYYYMMDD_*.mp4
            r"^PANO_\d{8}_.*\.jpg$",  # Matches PANO_YYYYMMDD_*.jpg
        ]

        matching_files = []

        # Iterate over all files in the selected folder
        for filename in os.listdir(folder_path):
            # Check if the filename matches any of the patterns
            if any(re.match(pattern, filename) for pattern in patterns):
                matching_files.append(filename)

        self.step_increment = self.__determine_progress_bar_step_increment(
            len(matching_files)
        )
        self.progress_bar.step(self.step_increment)

        logging.info(f"Found {len(matching_files)} matching files")

        return matching_files

    def move_files(
        self, grouped_files: Dict[str, List[str]], root_folder: Path
    ) -> Tuple[int, int]:
        """
        Moves files into their corresponding folders based on the grouping.

        Parameters:
        - grouped_files (dict): A dictionary where the key is the folder name and the value is a list of file paths.
        - destination_folder (str): The root folder where grouped folders will be created.

        :returns
        Number of successfully and unsuccessfully moved files.

        Example structure of `grouped_files`:
        {
            '2023-09-01': ['file1.jpg', 'file2.jpg'],
            '2023-09-02': ['file3.jpg']
        }
        """
        successes = 0
        failures = 0
        for folder_name, files in grouped_files.items():
            # Create the destination directory if it doesn't exist
            target_folder = os.path.join(root_folder, folder_name)
            os.makedirs(target_folder, exist_ok=True)
            for file_path in files:
                try:
                    source_path = os.path.join(root_folder, file_path)
                    # Move the file to the target folder
                    shutil.move(source_path, target_folder)
                    successes += 1
                    logging.info(f"Moved {file_path} to {target_folder}")
                except Exception as e:
                    failures += 1
                    logging.warning(f"Failed to move {file_path}: {e}")

        self.progress_bar.step(self.step_increment)
        return successes, failures

    def group_files_by_date(
        self, file_list: List[str], grouping: GroupingLevel
    ) -> Dict[str, List[str]]:
        """
        Groups files by date based on the filename and the specified grouping level.

        Parameters:
        - file_list: List of filenames to be grouped.
        - grouping: The level of grouping (GroupingLevel).

        Returns:
        - A dictionary where the keys are the date groups and the values are lists of filenames in each group.
        """
        grouped_files = defaultdict(list)
        for filename in file_list:
            date_part = self.__extract_date_part(filename, grouping)
            if date_part:
                grouped_files[date_part].append(filename)

        self.progress_bar.step(self.step_increment)
        logging.info(
            f"Number of groups: {len(grouped_files)}\nGroups themselves: {grouped_files.keys()}"
        )
        return dict(grouped_files)

    def __extract_date_part(self, filename: str, grouping: GroupingLevel) -> str:
        """
        Extracts the date part from the filename based on the grouping level.

        Parameters:
        - filename: The name of the file.
        - grouping: The level of grouping (GroupingLevel).

        Returns:
        - The extracted date part as a string.
        """
        # Extract the date part from the filename
        # Assuming filenames are in the format: PREFIX_YYYYMMDD_rest.ext
        parts = filename.split("_")
        date_part = parts[1]  # YYYYMMDD

        year = date_part[:4]
        month = date_part[4:6]
        day = date_part[6:8]

        if grouping == GroupingLevel.YYYY:
            return year
        elif grouping == GroupingLevel.YYYYMM:
            return f"{year}.{month}"
        elif grouping == GroupingLevel.YYYYMMDD:
            return f"{year}.{month}.{day}"

    def __display_message_box(self, successes: int = 20, failures: int = 5) -> None:
        title = "Przetwarzanie zakończone"
        msg = f"Przeniesiono {successes} z {successes + failures} plików"
        if not failures:
            messagebox.showinfo(title, msg)
        else:
            messagebox.showwarning(title, msg)

    def __determine_progress_bar_step_increment(self, files_count: int):
        if files_count:
            return 33.3
        return self.step_increment

    def __update_label(self, desired_text: str) -> None:
        self.progress_bar_label["text"] += f"\n\n{desired_text}"


def organize_photos() -> None:
    logging.basicConfig(level=logging.INFO)
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    organize_photos()
