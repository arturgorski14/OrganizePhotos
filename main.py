import tkinter as tk

from select_folder import select_folder


def main():
    root_window = tk.Tk()

    btn = tk.Button(
        root_window,
        text="Wybierz folder ze zdjęciami!",
        command=select_folder,
        padx=50,
        pady=50,
    )
    btn.pack()

    root_window.mainloop()


if __name__ == "__main__":
    main()
