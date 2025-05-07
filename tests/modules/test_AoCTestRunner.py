import pytest
from unittest.mock import patch, MagicMock
from pysleigh.modules.run_test import AoCTestRunner
from pysleigh.utilities.date import AoCDate


@pytest.mark.unit
class TestAoCTestRunner:

    def test_specific_test_runs_when_file_exists(self):
        runner = AoCTestRunner(AoCDate(2022, 1))
        with patch("pathlib.Path.exists", return_value=True), \
             patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            assert runner.run_specific_test() is True

    def test_specific_test_warns_if_missing(self):
        runner = AoCTestRunner(AoCDate(2022, 1))
        with patch("pathlib.Path.exists", return_value=False):
            assert runner.run_specific_test() is False

    def test_run_year_tests_executes_for_existing_dir(self):
        runner = AoCTestRunner(AoCDate(2022, 1))
        with patch("pathlib.Path.exists", return_value=True), \
             patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            assert runner.run_year_tests(2022) is True

    def test_run_year_tests_warns_if_dir_missing(self):
        runner = AoCTestRunner(AoCDate(2022, 1))
        with patch("pathlib.Path.exists", return_value=False):
            assert runner.run_year_tests(2022) is False

    def test_run_all_tests_runs_when_dir_exists(self):
        runner = AoCTestRunner()
        with patch("pathlib.Path.exists", return_value=True), \
             patch("subprocess.run") as mock_run:
            mock_run.return_value.returncode = 0
            assert runner.run_all_tests() is True

    def test_run_all_tests_logs_if_missing(self):
        runner = AoCTestRunner()
        with patch("pathlib.Path.exists", return_value=False):
            assert runner.run_all_tests() is False

    def test_run_dispatches_specific_if_date_set(self):
        runner = AoCTestRunner(AoCDate(2022, 1))
        with patch.object(runner, "run_specific_test", return_value=True) as mock:
            assert runner.run()
            mock.assert_called_once()

    def test_run_dispatches_all_if_no_date(self):
        runner = AoCTestRunner()
        with patch.object(runner, "run_all_tests", return_value=True) as mock:
            assert runner.run()
            mock.assert_called_once()
