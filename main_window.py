import tkinter as tk
from tkinter import messagebox

from constants import (ACTIVE_BUTTON_COLOR, DEFAULT_BUTTON_COLOR,
                       USER_ACTION_NEEDED_COLOR, ButtonState, GroupingLevel)
from move_files_to_main_folder import move_files_to_main_folder
from organize_photos import OrganizePhotos
from select_folder import select_folder


class MainWindow(tk.Tk):
    def __init__(self, default_grouping_level_value: str):
        super().__init__()
        self.title("Organizer zdjęć")
        self.geometry("400x300")

        top_frame = tk.Frame(self, padx=10, pady=10, bd=2, relief="groove")
        top_frame.pack(side="top", fill="x")  # Pack at the top and fill the width
        self.grouping_section_btn = tk.Button(
            top_frame,
            text="Grupowanie",
            state="normal",
            command=self.show_grouping_widgets,
            bg=ACTIVE_BUTTON_COLOR,
        )
        self.flattening_section_btn = tk.Button(
            top_frame,
            text="Spłaszczanie",
            state="normal",
            command=self.show_flattening_widgets,
        )
        self.grouping_section_btn.pack(side="left", expand=True, fill="both")
        self.flattening_section_btn.pack(side="left", expand=True, fill="both")

        bottom_frame = tk.Frame(self, padx=10, pady=10, bd=2, relief="groove")
        bottom_frame.pack(
            side="bottom", fill="both", expand=True
        )  # Pack at the bottom and fill the remaining space

        folder_frame = tk.Frame(bottom_frame, padx=10, pady=10, bd=2, relief="groove")
        folder_frame.pack(side="top", fill="both", expand=True)
        self.folder_label = tk.Label(folder_frame, text="Brak wybranego folderu")
        self.folder_btn = tk.Button(
            folder_frame,
            text="Wybierz folder!",
            command=self.select_folder,
            bg=USER_ACTION_NEEDED_COLOR,
        )
        self.folder_btn.pack()
        self.folder_label.pack()

        concrete_frame = tk.Frame(bottom_frame, padx=10, pady=10, bd=2, relief="groove")
        concrete_frame.pack(side="top", fill="both", expand=True)
        self.flattening_label = tk.Label(
            concrete_frame,
            text="Przenosi wszystkie pliki do wybranego folderu\n"
            "Pomija pliki o tych samych nazwach\n"
            "Usuwa puste foldery.",
        )
        self.dropdown_label = tk.Label(concrete_frame, text="Wybierz sposób grupowania")
        self.grouping_variable = tk.StringVar(concrete_frame)
        self.grouping_variable.set(default_grouping_level_value)
        self.dropdown = tk.OptionMenu(
            concrete_frame,
            self.grouping_variable,
            *[option.value for option in GroupingLevel],
        )
        self.dropdown_label.pack()
        self.dropdown.pack()

        self.run_button_frame = tk.Frame(
            bottom_frame, padx=10, pady=10, bd=2, relief="groove"
        )
        self.run_button_frame.pack(side="top", fill="both", expand=True)
        self.run_button = tk.Button(
            self.run_button_frame,
            text="Uruchom!",
            command=self.create_new_window_and_organize,
            state="disabled",
        )
        self.run_button.pack()

    def show_grouping_widgets(self):
        self.dropdown_label.pack()
        self.dropdown.pack()
        self.flattening_label.pack_forget()
        self.grouping_section_btn["bg"] = ACTIVE_BUTTON_COLOR
        self.flattening_section_btn["bg"] = DEFAULT_BUTTON_COLOR
        self.run_button.configure(command=self.create_new_window_and_organize)

    def show_flattening_widgets(self):
        self.dropdown_label.pack_forget()
        self.dropdown.pack_forget()
        self.flattening_label.pack()
        self.grouping_section_btn["bg"] = DEFAULT_BUTTON_COLOR
        self.flattening_section_btn["bg"] = ACTIVE_BUTTON_COLOR
        self.run_button.configure(command=self.flatten_files_within_folder)

    def select_folder(self) -> None:
        folder_path = select_folder()
        if not folder_path:
            self.folder_label["text"] = "Brak wybranego folderu"
            self.folder_btn["text"] = "Wybierz folder!"
            self.folder_btn["bg"] = USER_ACTION_NEEDED_COLOR
            self.run_button["bg"] = DEFAULT_BUTTON_COLOR
            self.__change_button_state(self.run_button, ButtonState.disabled)
            return
        self.folder_label["text"] = folder_path
        self.folder_btn["text"] = "Wybrany folder:"
        self.folder_btn["bg"] = DEFAULT_BUTTON_COLOR
        self.run_button["bg"] = ACTIVE_BUTTON_COLOR
        self.__change_button_state(self.run_button, ButtonState.normal)

    def create_new_window_and_organize(self) -> None:
        self.__change_button_state(self.run_button, ButtonState.disabled)
        self.__change_button_state(self.folder_btn, ButtonState.disabled)

        command = OrganizePhotos(
            self.folder_label["text"],
            self.__convert_grouping_value_back_to_enum(),
        )
        command.group()

        self.__change_button_state(self.run_button, ButtonState.normal)
        self.__change_button_state(self.folder_btn, ButtonState.normal)

    def flatten_files_within_folder(self) -> None:
        self.__change_button_state(self.run_button, ButtonState.disabled)
        self.__change_button_state(self.folder_btn, ButtonState.disabled)

        moved, skipped, failures, total = move_files_to_main_folder(
            self.folder_label["text"]
        )
        self.__display_message_box(moved, skipped, failures, total)

        self.__change_button_state(self.run_button, ButtonState.normal)
        self.__change_button_state(self.folder_btn, ButtonState.normal)

    def __convert_grouping_value_back_to_enum(self) -> GroupingLevel:
        grouping_level = self.grouping_variable.get()
        mapping = {
            GroupingLevel.YYYY.value: GroupingLevel.YYYY,
            GroupingLevel.YYYYMM.value: GroupingLevel.YYYYMM,
            GroupingLevel.YYYYMMDD.value: GroupingLevel.YYYYMMDD,
        }
        return mapping[grouping_level]

    def __change_button_state(
        self, button: tk.Button, desired_state: ButtonState
    ) -> None:
        button["state"] = desired_state.value

    def __display_message_box(
        self, successes: int = 0, skipped: int = 0, failures: int = 0, total: int = 0
    ) -> None:
        title = "Przetwarzanie zakończone"
        msg = f"Przeniesiono {successes} z {total} plików."
        if skipped:
            msg += f"\nPominięto {skipped} plików."
        if failures:
            msg += f"\nBłędów przy przenoszeniu {failures} plików."
            messagebox.showwarning(title, msg)
        else:
            messagebox.showinfo(title, msg)
