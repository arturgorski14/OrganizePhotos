import logging

from organize_photos_app import OrganizePhotos


def main():
    app = OrganizePhotos()
    app.mainloop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
