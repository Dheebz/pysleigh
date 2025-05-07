import pytest
from pathlib import Path
from pysleigh.utilities.config import AoCConfig


@pytest.mark.unit
class TestAoCConfig:
    def test_valid_config_loads(self, tmp_path):
        cfg_path = tmp_path / "config.toml"
        cfg_path.write_text("""
        [session_cookie]
        session_cookie = "abc123"

        [inputs]
        path = "~/input/"
        format = "day_{day}.txt"
        """)
        cfg = AoCConfig(config_path=str(cfg_path))
        assert cfg.config["session_cookie"]["session_cookie"] == "abc123"

    def test_missing_config_raises_runtime(self, tmp_path):
        cfg_path = tmp_path / "nonexistent.toml"
        with pytest.raises(RuntimeError) as excinfo:
            AoCConfig(config_path=str(cfg_path))
        assert "Edit your config at:" in str(excinfo.value)

    def test_config_warns_on_missing_session(self, tmp_path, caplog):
        cfg_path = tmp_path / "config.toml"
        cfg_path.write_text("""
        [session_cookie]
        session_cookie = ""
        """)
        AoCConfig(config_path=str(cfg_path))
        assert "Session cookie is empty." in caplog.text

    def test_invalid_toml_fails_gracefully(self, tmp_path, caplog):
        cfg_path = tmp_path / "config.toml"
        cfg_path.write_text("[this is not valid TOML")
        cfg = AoCConfig(config_path=str(cfg_path))
        assert cfg.config == {}
        assert "Failed to parse config" in caplog.text
