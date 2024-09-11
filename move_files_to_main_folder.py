import os
import shutil


def move_files_to_main_folder(main_folder: str):
    """
    Przenosi wszystkie pliki z podfolderów do głównego folderu.

    :param main_folder: Ścieżka do głównego folderu, z którego pliki będą przenoszone
                        i do którego trafią.
    """
    # Przejście przez wszystkie podfoldery i pliki

    for root, dirs, files in os.walk(main_folder):
        # Sprawdź, czy nie jesteśmy w folderze głównym (pomijamy folder główny)
        if root != main_folder:
            for file in files:
                # Pełna ścieżka do pliku
                file_path = os.path.join(root, file)

                # Ścieżka docelowa w folderze głównym
                destination_path = os.path.join(main_folder, file)

                # Przeniesienie pliku do folderu głównego
                shutil.move(file_path, destination_path)
