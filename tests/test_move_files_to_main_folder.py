import os
import tempfile

import pytest

from move_files_to_main_folder import move_files_to_main_folder


@pytest.fixture
def setup_test_environment():
    """
    Tworzy tymczasowy folder z podfolderami i opcjonalnie plikami o tych samych nazwach w różnych podfolderach.
    Zwraca ścieżkę do folderu głównego i ścieżki do plików.

    :param same_file_names: Jeśli True, pliki będą miały te same nazwy w różnych podfolderach.
    """

    def _setup_test_environment(same_file_names=False):
        with tempfile.TemporaryDirectory() as main_folder:
            subfolder1 = os.path.join(main_folder, "podfolder1")
            subfolder2 = os.path.join(main_folder, "podfolder2")
            subfolder3 = os.path.join(subfolder2, "podfolder_podfolderu")
            os.makedirs(subfolder1)
            os.makedirs(subfolder2)
            os.makedirs(subfolder3)

            if same_file_names:
                # Pliki o tych samych nazwach w różnych podfolderach
                file1_path = os.path.join(subfolder1, "plik.txt")
                file2_path = os.path.join(subfolder2, "plik.txt")
                file3_path = os.path.join(subfolder3, "plik.txt")
            else:
                # Pliki o różnych nazwach w różnych podfolderach
                file1_path = os.path.join(subfolder1, "plik1.txt")
                file2_path = os.path.join(subfolder2, "plik2.txt")
                file3_path = os.path.join(subfolder3, "plik3.txt")

            with open(file1_path, "w") as f:
                f.write("To jest plik 1 z podfolder1")
            with open(file2_path, "w") as f:
                f.write("To jest plik 2 z podfolder2")
            with open(file3_path, "w") as f:
                f.write("To jest plik 3 z podfolder_podfolderu")

            yield main_folder, file1_path, file2_path, file3_path

    return _setup_test_environment


def test_move_files_to_main_folder(setup_test_environment):
    # Otrzymujemy dane z fixture z plikami o różnych nazwach
    setup_env = setup_test_environment(same_file_names=False)
    main_folder, file1_path, file2_path, file3_path = next(setup_env)

    # Wywołanie funkcji, która przenosi pliki
    move_files_to_main_folder(main_folder)

    # Sprawdzanie, czy pliki zostały przeniesione do folderu głównego
    assert os.path.isfile(os.path.join(main_folder, "plik1.txt"))
    assert os.path.isfile(os.path.join(main_folder, "plik2.txt"))
    assert os.path.isfile(os.path.join(main_folder, "plik3.txt"))

    # Upewnienie się, że pliki zostały usunięte z podfolderów
    assert not os.path.exists(file1_path)
    assert not os.path.exists(file2_path)
    assert not os.path.exists(file3_path)


def test_move_files_with_same_names(setup_test_environment):
    # Otrzymujemy dane z fixture z plikami o tych samych nazwach
    setup_env = setup_test_environment(same_file_names=True)
    main_folder, file1_path, file2_path, file3_path = next(setup_env)

    # Wywołanie funkcji, która przenosi pliki
    move_files_to_main_folder(main_folder)

    # Sprawdzanie, czy przynajmniej jeden plik został przeniesiony
    destination_file_path = os.path.join(main_folder, "plik.txt")
    assert os.path.isfile(destination_file_path)

    # Odczytanie zawartości przeniesionego pliku, aby sprawdzić, który z plików został zachowany
    with open(destination_file_path, "r") as f:
        content = f.read()

    # Sprawdzamy, czy plik w folderze głównym został nadpisany
    assert content in [
        "To jest plik 1 z podfolder1",
        "To jest plik 2 z podfolder2",
        "To jest plik 3 z podfolder_podfolderu",
    ]

    # Upewniamy się, że wszystkie pliki zostały usunięte z podfolderów
    assert not os.path.exists(file1_path)
    assert not os.path.exists(file2_path)
    assert not os.path.exists(file3_path)
