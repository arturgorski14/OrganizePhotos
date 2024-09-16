import logging
import os
import shutil
from pathlib import Path
from typing import Tuple


def move_files_to_main_folder(
    source_folder: str | Path, resolution: str = "skip"
) -> Tuple[int, int, int, int]:
    """
    Przenosi wszystkie pliki z podfolderów do folderu głównego.
    Jeśli plik o tej samej nazwie już istnieje, operacja jest pomijana.
    Po przeniesieniu plików usuwa puste podfoldery.

    Zlicza liczbę przeniesionych plików oraz całkowitą liczbę plików.

    :param source_folder: Ścieżka do folderu źródłowego.
    :param resolution: Strategia rozwiązywania konfliktów (tylko 'skip' jest obsługiwana).
    :return: Krotka z liczbą przeniesionych plików oraz całkowitą liczbą plików.
    """
    assert resolution == "skip", "Obecnie obsługiwana jest tylko strategia 'skip'."
    assert os.path.isdir(source_folder), f"Brak wybranego folderu - {source_folder}!"

    total_files_count = 0
    moved_files_count = 0
    skipped_files_count = 0
    failures_count = 0

    # Przenoszenie plików
    for root, dirs, files in os.walk(source_folder, topdown=False):
        total_files_count += len(files)
        for file_name in files:
            source_file_path = os.path.join(root, file_name)
            dest_file_path = os.path.join(source_folder, file_name)

            if not os.path.exists(dest_file_path):
                try:
                    shutil.move(source_file_path, dest_file_path)
                    moved_files_count += 1
                    logging.info(f"Moved {source_file_path} to {dest_file_path}")
                except Exception as e:
                    failures_count += 1
                    logging.warning(f"Failed to move {source_file_path}: {e}")
            else:
                skipped_files_count += 1
                logging.warning(
                    f"File with the same name exists in {source_folder}. Skipping {source_file_path}"
                )

    # Usuwanie pustych podfolderów
    for root, dirs, files in os.walk(source_folder, topdown=False):
        for dir_name in dirs:
            dir_path = os.path.join(root, dir_name)
            if not os.listdir(dir_path):  # Sprawdzamy, czy katalog jest pusty
                os.rmdir(dir_path)  # Usuwamy pusty katalog

    return moved_files_count, skipped_files_count, failures_count, total_files_count
