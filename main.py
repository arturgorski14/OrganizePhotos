import logging

from organize_photos import MainWindow


def main():
    app = MainWindow()
    app.mainloop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
