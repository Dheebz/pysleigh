import toml
from pathlib import Path
from typing import Dict

from pysleigh.utilities.logger import AoCLogger


class AoCConfig:
    logger = AoCLogger().get_logger()
    DEFAULT_CONFIG_PATH = Path("~/.config/pysleigh/config.toml").expanduser()

    def __init__(self, config_path: str | None = None):
        self.config_path = (
            Path(config_path).expanduser() if config_path else self.DEFAULT_CONFIG_PATH
        )
        if not self.check_exists():
            self.logger.warning(
                f"Config file not found at '{self.config_path}'. Creating from template."
            )
            self.__write_default_template()
            self.logger.error("Please edit the config file before running commands.")
            raise RuntimeError(f"Edit your config at: {self.config_path}")

        self.config: Dict[str, Dict[str, str]] = self.load_config()
        self.validate()

    def check_exists(self) -> bool:
        return self.config_path.exists()

    def __write_default_template(self) -> None:
        default_config = """
            [session_cookie]
            session_cookie = ""

            [inputs]
            path = "~/Workspace/advent-of-code/input/"
            format = "year_{year}/input_{year}_day_{day:02d}.txt"

            [articles]
            path = "~/Workspace/advent-of-code/articles/"
            format = "year_{year}/article_{year}_day_{day:02d}.md"

            [solutions]
            path = "~/Workspace/advent-of-code/solutions/python/"
            format = "year_{year}/solution_{year}_day_{day:02d}.py"

            [tests]
            path = "~/Workspace/advent-of-code/tests/python/"
            format = "year_{year}/test_{year}_day_{day:02d}.py"

            [answers]
            path = "~/Workspace/advent-of-code/answers/"
            format = "year_{year}/answer_{year}_day{day:02d}.txt"

            [template] # Optional
            solution_path = "~/.config/pysleigh/solution_template.py"
            test_path = "~/.config/pysleigh/test_template.py"
            """.strip().replace("            ", "")

        try:
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            self.config_path.write_text(default_config.strip())
        except Exception as e:
            self.logger.error(f"Failed to write default config template: {e}")

    def load_config(self) -> Dict[str, Dict[str, str]]:
        try:
            return toml.loads(self.config_path.read_text())
        except Exception as e:
            self.logger.error(f"Failed to parse config: {e}")
            return {}

    def validate(self) -> bool:
        if not self.config.get("session_cookie", {}).get("session_cookie"):
            self.logger.warning("Session cookie is empty.")
            return False
        return True
