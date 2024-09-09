import pytest

from organize_photos import GroupingLevel, OrganizePhotos

PROGRESS_BAR_LENGTH = 300
NUMBER_OF_STEPS = 3


@pytest.mark.xfail(reason="Zmiana koncepcji progress bara")
class TestDetermineProgressBarStepIncrement:
    @pytest.fixture
    def setup_app(self, tmp_path):
        # Setup the OrganizePhotos instance for testing
        app = OrganizePhotos(
            folder_path=str(tmp_path), grouping_level=GroupingLevel.YYYY
        )
        return app

    @pytest.mark.parametrize(
        "files_count, expected_increment",
        [
            (1, (PROGRESS_BAR_LENGTH - 0.1) / NUMBER_OF_STEPS / 1),
            (2, (PROGRESS_BAR_LENGTH - 0.1) / NUMBER_OF_STEPS / 2),
            (10, (PROGRESS_BAR_LENGTH - 0.1) / NUMBER_OF_STEPS / 10),
            (100, (PROGRESS_BAR_LENGTH - 0.1) / NUMBER_OF_STEPS / 100),
        ],
    )
    def test_progress_bar_step_increment(
        self, setup_app, files_count, expected_increment
    ):
        app = setup_app
        # Call the private method
        result = app._OrganizePhotos__determine_progress_bar_step_increment(files_count)

        # Check if the result matches the expected value
        assert (
            result == expected_increment
        ), f"Expected {expected_increment}, got {result}"

    def test_progress_bar_step_increment_zero_files(self, setup_app):
        app = setup_app
        expected_increment = app.PROGRESS_BAR_LENGTH - 0.1

        # Call the private method with files_count = 0
        result = app._OrganizePhotos__determine_progress_bar_step_increment(0)

        assert (
            result == expected_increment
        ), f"Expected {expected_increment}, got {result}"
