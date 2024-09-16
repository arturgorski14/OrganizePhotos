import os
from pathlib import WindowsPath

import pytest

from move_files_to_main_folder import move_files_to_main_folder


@pytest.fixture
def setup_test_environment(tmp_path):
    """
    Tworzy tymczasowy folder z podfolderami i plikami.
    Zwraca ścieżkę do folderu głównego i słownik z plikami.
    """

    def _setup_test_environment():

        subfolder1 = create_path(tmp_path, "podfolder1")
        subfolder2 = create_path(tmp_path, "podfolder2")
        subfolder3 = create_path(subfolder2, "podfolder_podfolderu")
        os.makedirs(subfolder1)
        os.makedirs(subfolder2)
        os.makedirs(subfolder3)

        # Pliki o różnych nazwach
        file1_path = create_path(subfolder1, "plik1.txt")
        file2_path = create_path(subfolder2, "plik2.txt")
        file3_path = create_path(subfolder3, "plik3.txt")

        # Pliki o tych samych nazwach
        same_name_file1_path = create_path(subfolder1, "plik.txt")
        same_name_file2_path = create_path(subfolder2, "plik.txt")
        same_name_file3_path = create_path(subfolder3, "plik.txt")

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

        return tmp_path, {
            "different_names": [file1_path, file2_path, file3_path],
            "same_names": [
                same_name_file1_path,
                same_name_file2_path,
                same_name_file3_path,
            ],
        }

    return _setup_test_environment


def create_path(*args):
    return WindowsPath(os.path.join(*args))


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

    # Sprawdzamy, że tylko pierwszy plik z tych o jednakowych nazwach zostal przeniesiony
    moved_filename = same_names[0]
    assert not os.path.isfile(
        moved_filename
    ), f"{moved_filename} should be moved to main folder"
    moved_filename = create_path(main_folder, os.path.basename(moved_filename))
    assert os.path.isfile(
        moved_filename
    ), f"{moved_filename} should be inside main folder"

    for file_path in same_names[1:]:
        assert os.path.isfile(file_path), f"{file_path} is not a file {type(file_path)}"

    # Upewniamy się, że pliki o różnych nazwach zostały usunięte z podfolderów
    for file_path in different_names:
        assert not os.path.exists(file_path)

    # Sprawdzamy liczbę przeniesionych plików i całkowitą liczbę plików
    assert moved_files_count == len(different_names) + 1  # include moved_filename
    assert total_files_count == len(different_names) + len(same_names)
