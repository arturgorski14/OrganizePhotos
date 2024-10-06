import logging
import os
import re
import shutil
from collections import defaultdict
from pathlib import Path
from tkinter import messagebox
from typing import Dict, List, Tuple

from constants import PATTERNS, GroupingLevel


class OrganizePhotos:

    def __init__(
        self,
        folder_path: str,
        grouping_level: GroupingLevel,
    ):
        self.folder_path = folder_path
        self.grouping_level = grouping_level

    def group(self) -> None:
        folder_path = self.folder_path
        grouping_level = self.grouping_level

        files = self.get_matching_files(folder_path)
        grouped_files = self.group_files_by_date(files, grouping_level)
        successes, failures = self.move_files(grouped_files, Path(folder_path))

        self.__display_message_box(successes, failures)

    def get_matching_files(self, folder_path) -> List[str]:
        if not folder_path:
            return []

        matching_files = []

        # Iterate over all files in the selected folder
        files = os.listdir(folder_path)
        for filename in files:
            # Check if the filename matches any of the patterns
            if any(re.match(pattern, filename) for pattern in PATTERNS):
                matching_files.append(filename)

        logging.info(f"Found {len(matching_files)} matching files out of {len(files)}")

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
            folder_name = self.__create_folder_name(filename, grouping)
            if folder_name:
                grouped_files[folder_name].append(filename)

        logging.info(
            f"Number of groups: {len(grouped_files)}\nGroups themselves: {grouped_files.keys()}"
        )
        return dict(grouped_files)

    def __create_folder_name(self, filename: str, grouping: GroupingLevel) -> str:
        """
        Extracts the date part from the filename based on the grouping level.

        Parameters:
        - filename: The name of the file.
        - grouping: The level of grouping (GroupingLevel).

        Returns:
        - The extracted date part as a string.
        """
        date_part = self.__extract_date_part(filename)

        year = date_part[:4]
        month = date_part[4:6]
        day = date_part[6:8]

        mapping = {
            GroupingLevel.YYYY: f"{year}",
            GroupingLevel.YYYYMM: f"{year}.{month}",
            GroupingLevel.YYYYMMDD: f"{year}.{month}.{day}",
        }
        return mapping[grouping]

    def __extract_date_part(self, filename: str) -> str:
        first_digit_position = [x.isdigit() for x in filename].index(True)
        cleaned_date: str = filename[first_digit_position:]
        return cleaned_date[:8]

    def __display_message_box(self, successes: int = 20, failures: int = 5) -> None:
        title = "Przetwarzanie zakończone"
        msg = f"Przeniesiono {successes} z {successes + failures} plików"
        if not failures:
            messagebox.showinfo(title, msg)
        else:
            messagebox.showwarning(title, msg)
