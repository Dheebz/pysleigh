import pytest
from unittest.mock import patch, MagicMock
from pysleigh.utilities.session import AoCSession
from pysleigh.utilities.config import AoCConfig


@pytest.mark.unit
class TestAoCSession:
    def test_session_cookie_injection(self):
        config = AoCConfig()
        config.session_cookie = "abc123"
        session = AoCSession(config)
        assert session.session.cookies.get("session") != ""

    def test_warn_on_missing_cookie(self, caplog):
        with patch("pysleigh.utilities.config.AoCConfig") as MockConfig:
            MockConfig.return_value.config = {"session_cookie": {"session_cookie": ""}}
            AoCSession(config=MockConfig())
        assert "No session cookie provided" in caplog.text

    def test_get_delegates_to_requests(self):
        with patch("requests.Session") as MockSession:
            mock_resp = MagicMock(status_code=200)
            mock_sess = MockSession.return_value
            mock_sess.get.return_value = mock_resp

            s = AoCSession()
            resp = s.get("https://example.com")
            mock_sess.get.assert_called_once_with("https://example.com")
            assert resp.status_code == 200

    def test_post_delegates_to_requests(self):
        with patch("requests.Session") as MockSession:
            mock_resp = MagicMock(status_code=201)
            mock_sess = MockSession.return_value
            mock_sess.post.return_value = mock_resp

            s = AoCSession()
            resp = s.post("https://example.com", data={"key": "value"})
            mock_sess.post.assert_called_once_with(
                "https://example.com", data={"key": "value"}
            )
            assert resp.status_code == 201
