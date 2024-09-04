import os
import shutil


def move_files(grouped_files, destination_folder):
    """
    Moves files into their corresponding folders based on the grouping.

    Parameters:
    - grouped_files (dict): A dictionary where the key is the folder name and the value is a list of file paths.
    - destination_folder (str): The root folder where grouped folders will be created.

    Example structure of `grouped_files`:
    {
        '2023-09-01': ['/path/to/file1.jpg', '/path/to/file2.jpg'],
        '2023-09-02': ['/path/to/file3.jpg']
    }
    """
    for folder_name, files in grouped_files.items():
        # Create the destination directory if it doesn't exist
        target_folder = os.path.join(destination_folder, folder_name)
        os.makedirs(target_folder, exist_ok=True)

        for file_path in files:
            try:
                # Move the file to the target folder
                shutil.move(file_path, target_folder)
                print(f"Moved {file_path} to {target_folder}")
            except Exception as e:
                print(f"Failed to move {file_path}: {e}")
