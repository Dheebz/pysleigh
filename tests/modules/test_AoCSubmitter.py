import pytest
from unittest.mock import patch, MagicMock
from pysleigh.modules.submit_solution import AoCSubmitter
from pysleigh.utilities.date import AoCDate


@pytest.mark.unit
class TestAoCSubmitter:

    def test_submit_success_200(self):
        date = AoCDate(2022, 1)
        submitter = AoCSubmitter(date)

        with patch.object(submitter.session, "post") as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.text = "<article><p>Thanks!</p></article>"
            response = submitter.submit(1, "123")
            assert "Thanks!" in response

    def test_submit_fails_logs_error(self, caplog):
        date = AoCDate(2022, 1)
        submitter = AoCSubmitter(date)

        with patch.object(submitter.session, "post") as mock_post:
            mock_post.return_value.status_code = 500
            mock_post.return_value.text = "fail"
            result = submitter.submit(1, "999")
            assert "HTTP 500" in caplog.text
            assert "Error: HTTP 500" in result

    def test_compute_answer_imports_correctly(self):
        date = AoCDate(2022, 1)
        submitter = AoCSubmitter(date)

        with patch("pysleigh.modules.submit_solution.importlib.import_module") as mock_import:
            mock_mod = MagicMock()
            mock_mod.Solution.return_value.part1.return_value = 42
            mock_mod.Solution.return_value.part2.return_value = 99
            mock_import.return_value = mock_mod

            assert submitter.compute_answer(1) == "42"
            assert submitter.compute_answer(2) == "99"

    @pytest.mark.parametrize("html,expected", [
        ("<article><p>That's the right answer!</p></article>", ("✅ CORRECT", "That's the right answer!")),
        ("<article><p>That's not the right answer.</p></article>", ("❌ INCORRECT", "That's not the right answer.")),
        ("<article><p>You gave an answer too recently</p></article>", ("⏱ COOLDOWN", "You gave an answer too recently")),
        ("<article><p>Did you already complete it?</p></article>", ("📎 ALREADY SUBMITTED", "Did you already complete it?")),
        # Not a real condition but for testing purposes we want to check the default case
        ("<article><p>Unknown response</p></article>", ("❗ UNKNOWN", "Unknown response")),
        ("<article><p>Some other message</p></article>", ("❗ UNKNOWN", "Some other message")),])
    def test_parse_response(self, html, expected):
        date = AoCDate(2022, 1)
        submitter = AoCSubmitter(date)
        assert submitter.parse_response(html) == expected
