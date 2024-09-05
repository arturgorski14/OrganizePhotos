import logging
import tkinter as tk
from pathlib import Path
from tkinter import messagebox, ttk

from get_matching_files import get_matching_files
from group_files_by_date import GroupingLevel, group_files_by_date
from move_files import move_files
from select_folder import select_folder


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Organizer zdjęć")
        self.geometry("300x300")

        self.folder_label = tk.Label(self, text="Brak wybranego folderu")
        self.folder_label.grid(row=0, column=1)
        self.folder_btn = tk.Button(
            self, text="Wybierz folder!", command=self.select_folder
        )
        self.folder_btn.grid(row=0, column=0)

        # Create a variable to hold the selected grouping level
        self.grouping_var = tk.IntVar(value=1)  # Default to GroupingLevel.YYYY

        # Create radio buttons for grouping options
        tk.Radiobutton(self, text="Po roku", variable=self.grouping_var, value=1).grid(
            row=1, column=0
        )
        tk.Radiobutton(
            self, text="Po roku i miesiącu", variable=self.grouping_var, value=2
        ).grid(row=1, column=1)
        tk.Radiobutton(
            self, text="Po roku, miesiącu i dniu", variable=self.grouping_var, value=3
        ).grid(row=1, column=2)

        tk.Label(self, text=self.grouping_var.get()).grid(row=2, column=0)

        # Create a StringVar to be used for the label's text
        self.grouping_text = tk.StringVar(value=self.get_grouping_text())
        tk.Label(self, textvariable=self.grouping_text).grid(row=2, column=0)

        # Trace changes to the grouping_var to update the label
        self.grouping_var.trace("w", self.update_label)

        tk.Button(self, text="Uruchom!", command=self.organize).grid(row=3, column=0)

        tk.Button(
            self, text="DEBUG - Display message", command=self.display_message_box
        ).grid(row=4, column=0)

    def select_folder(self) -> None:
        folder_path = select_folder()
        if not folder_path:
            self.folder_label["text"] = "Brak wybranego folderu"
            self.folder_btn["text"] = "Wybierz folder!"
            return
        self.folder_label["text"] = folder_path
        self.folder_btn["text"] = "Wybrany folder:"

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

    def update_label(self, *args):
        # Update the label text based on the current value of grouping_var
        self.grouping_text.set(self.get_grouping_text())

    def organize(self) -> None:
        folder_path = self.folder_label["text"]
        grouping_level = self.get_grouping_level()

        files = get_matching_files(folder_path)
        grouped_files = group_files_by_date(files, grouping_level)
        successes, failures = move_files(grouped_files, Path(folder_path))

        self.display_message_box(successes, failures)

    def display_message_box(self, successes: int = 20, failures: int = 5) -> None:
        title = "Przetwarzanie zakończone"
        msg = f"Przeniesiono {successes} z {successes+failures} plików"
        if not failures:
            messagebox.showinfo(title, msg)
        else:
            messagebox.showwarning(title, msg)


def organize_photos() -> None:
    logging.basicConfig(level=logging.INFO)
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    organize_photos()
