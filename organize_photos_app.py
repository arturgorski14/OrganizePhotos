import tkinter as tk
from tkinter import ttk

from get_matching_files import get_matching_files
from group_files_by_date import GroupingLevel, group_files_by_date
from select_folder import select_folder


class GreetingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Greeting Application")
        self.geometry("300x300")

        self.name_var = tk.StringVar()
        self.name_var.trace("w", self.create_greeting_message)

        self.create_widgets()

    def create_widgets(self):
        self.description_label = tk.Label(self, text="Enter your name:")
        self.description_label.grid(column=0, row=0)

        self.entry = tk.Entry(self, textvariable=self.name_var)
        self.entry.grid(column=1, row=0)
        self.entry.focus()

        self.greeting_label = tk.Label(self)
        self.greeting_label.grid(column=0, row=1, columnspan=2)

    def create_greeting_message(self, *args):
        name_entered = self.name_var.get()

        greeting_message = ""
        if name_entered != "":
            greeting_message = "Hello " + name_entered

        self.greeting_label["text"] = greeting_message


class OrganizePhotos(tk.Tk):
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

        tk.Button(
            self, text="Uruchom!", command=self.organize
        ).grid(row=3, column=0)

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
        files = get_matching_files(folder_path)
        grouping_level = self.get_grouping_level()

        grouped_files = group_files_by_date(
            files, grouping_level
        )

