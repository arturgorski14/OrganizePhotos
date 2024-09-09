import logging
import tkinter as tk
from tkinter import filedialog

logging.basicConfig(level=logging.INFO, format="%(message)s")


def select_folder():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    folder_path = filedialog.askdirectory()
    if folder_path:
        logging.info(f"Selected folder: {folder_path}")
    else:
        logging.info("No folder selected")
    return folder_path
