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

        # initialize variables
        self.grouping_var = tk.IntVar(value=1)  # Default to GroupingLevel.YYYY
        self.grouping_text = tk.StringVar(value=self.get_grouping_text())
        self.grouping_var.trace("w", self.update_label)

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
        debug_radio_choice_label = tk.Label(self, text=self.grouping_var.get())
        debug_radio_choice_label_text = tk.Label(self, textvariable=self.grouping_text)
        self.run_button = tk.Button(
            self, text="Uruchom!", command=self.create_new_window_and_organize, state="disabled"
        )

        # placement on the grid
        self.folder_label.grid(row=0, column=1)
        self.folder_btn.grid(row=0, column=0)
        radio_btn1.grid(row=1, column=0)
        radio_btn2.grid(row=1, column=1)
        radio_btn3.grid(row=1, column=2)
        debug_radio_choice_label.grid(row=2, column=0)
        debug_radio_choice_label_text.grid(row=2, column=0)
        self.run_button.grid(row=3, column=0)

    def select_folder(self) -> None:
        folder_path = select_folder()
        if not folder_path:
            self.folder_label["text"] = "Brak wybranego folderu"
            self.folder_btn["text"] = "Wybierz folder!"
            self.__change_button_state("disabled")
            return
        self.folder_label["text"] = folder_path
        self.folder_btn["text"] = "Wybrany folder:"
        self.__change_button_state("normal")

    def __change_button_state(self, desired_state: str) -> None:
        """
        :param desired_state: active, normal, disabled
        """
        self.run_button["state"] = desired_state


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

    def create_new_window_and_organize(self) -> None:
        if not OrganizePhotos.alive:
            second_window = OrganizePhotos(self.folder_label["text"], self.get_grouping_level())
            second_window.organize()


class OrganizePhotos(tk.Toplevel):
    alive = False

    def __init__(self, folder_path: str, grouping_level: GroupingLevel, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.config(width=300, height=200)
        self.title("Przenoszenie plików do podfolderów")
        self.focus()
        self.__class__.alive = True

        self.folder_path = folder_path
        self.grouping_level = grouping_level

        progress_bar = ttk.Progressbar(self, orient="horizontal", mode="indeterminate", length=300)
        self.progress_bar_label = tk.Label(self, text="Rozpoczynam.")

        progress_bar.pack(pady=20)
        self.progress_bar_label.pack(pady=10)

    def destroy(self):
        # Restore the attribute on close.
        self.__class__.alive = False
        return super().destroy()

    def organize(self) -> None:
        folder_path = self.folder_path
        grouping_level = self.grouping_level

        files = get_matching_files(folder_path)
        self.__update_label(f"{len(files)} plików może zostać przeniesionych.")
        grouped_files = group_files_by_date(files, grouping_level)
        self.__update_label(f"Liczba nowych folderów: {len(grouped_files)}\nI ich nazwy: {grouped_files.keys()}")
        successes, failures = move_files(grouped_files, Path(folder_path))
        self.__update_label(f"Przeniesiono {successes} z {successes + failures} plików")
        self.display_message_box(successes, failures)

    def display_message_box(self, successes: int = 20, failures: int = 5) -> None:
        title = "Przetwarzanie zakończone"
        msg = f"Przeniesiono {successes} z {successes + failures} plików"
        if not failures:
            messagebox.showinfo(title, msg)
        else:
            messagebox.showwarning(title, msg)

    def __update_label(self, desired_text: str) -> None:
        self.progress_bar_label["text"] += f"\n\n{desired_text}"


def organize_photos() -> None:
    logging.basicConfig(level=logging.INFO)
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    organize_photos()
