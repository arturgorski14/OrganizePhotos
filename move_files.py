import logging
import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple


def move_files(grouped_files: Dict[str, List[str]], root_folder: Path) -> Tuple[int, int]:
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
