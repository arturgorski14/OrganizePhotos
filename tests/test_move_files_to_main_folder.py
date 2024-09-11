import os
import tempfile

import pytest

from move_files_to_main_folder import move_files_to_main_folder


@pytest.fixture
def setup_test_environment():
    """
    Tworzy tymczasowy folder z podfolderami i plikami.
    Zwraca ścieżkę do folderu głównego i słownik z plikami.
    """

    def _setup_test_environment():
        with tempfile.TemporaryDirectory() as main_folder:
            subfolder1 = os.path.join(main_folder, "podfolder1")
            subfolder2 = os.path.join(main_folder, "podfolder2")
            subfolder3 = os.path.join(subfolder2, "podfolder_podfolderu")
            os.makedirs(subfolder1)
            os.makedirs(subfolder2)
            os.makedirs(subfolder3)

            # Pliki o różnych nazwach
            file1_path = os.path.join(subfolder1, "plik1.txt")
            file2_path = os.path.join(subfolder2, "plik2.txt")
            file3_path = os.path.join(subfolder3, "plik3.txt")

            # Pliki o tych samych nazwach
            same_name_file1_path = os.path.join(subfolder1, "plik.txt")
            same_name_file2_path = os.path.join(subfolder2, "plik.txt")
            same_name_file3_path = os.path.join(subfolder3, "plik.txt")

            # Tworzenie plików
            with open(file1_path, "w") as f:
                f.write("To jest plik 1 z podfolder1")
            with open(file2_path, "w") as f:
                f.write("To jest plik 2 z podfolder2")
            with open(file3_path, "w") as f:
                f.write("To jest plik 3 z podfolder_podfolderu")

            with open(same_name_file1_path, "w") as f:
                f.write("To jest plik o tej samej nazwie w podfolder1")
            with open(same_name_file2_path, "w") as f:
                f.write("To jest plik o tej samej nazwie w podfolder2")
            with open(same_name_file3_path, "w") as f:
                f.write("To jest plik o tej samej nazwie w podfolder3")

            return main_folder, {
                "different_names": [file1_path, file2_path, file3_path],
                "same_names": [
                    same_name_file1_path,
                    same_name_file2_path,
                    same_name_file3_path,
                ],
            }

    return _setup_test_environment


@pytest.mark.skip(reason="Poorly designed test. Needs functionality asap.")
def test_move_files_to_main_folder_skip(setup_test_environment):
    main_folder, files = setup_test_environment()
    different_names = files["different_names"]
    same_names = files["same_names"]

    moved_files_count, *_, total_files_count = move_files_to_main_folder(
        main_folder, resolution="skip"
    )

    # Sprawdzamy, że pliki o różnych nazwach zostały przeniesione
    assert os.path.isfile(os.path.join(main_folder, "plik1.txt"))
    assert os.path.isfile(os.path.join(main_folder, "plik2.txt"))
    assert os.path.isfile(os.path.join(main_folder, "plik3.txt"))

    # Sprawdzamy, że pliki o tych samych nazwach nie zostały przeniesione
    for file_path in same_names:
        assert os.path.isfile(file_path)

    # Upewniamy się, że pliki o różnych nazwach zostały usunięte z podfolderów
    for file_path in different_names:
        assert not os.path.exists(file_path)

    # Sprawdzamy liczbę przeniesionych plików i całkowitą liczbę plików
    assert moved_files_count == len(different_names)
    assert total_files_count == len(different_names) + len(same_names)
