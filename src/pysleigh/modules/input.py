from pathlib import Path
from pysleigh.utilities.config import AoCConfig
from pysleigh.utilities.logger import AoCLogger
from pysleigh.utilities.date import AoCDate
from pysleigh.utilities.session import AoCSession


class AoCInput:
    logger = AoCLogger().get_logger()
    BASE_URL = "https://adventofcode.com"
    DEFAULT_DATE = AoCDate._compute_max_date()
    DEFAULT_PATH = Path("~/Workspace/advent-of-code/inputs")

    def __init__(
        self, aoc_date: AoCDate | None = None, config: AoCConfig | None = None
    ):
        self.aoc_date = aoc_date or AoCDate(*self.DEFAULT_DATE)
        self.config = config or AoCConfig()
        self.input_path = self.get_input_path()
        self.url = self._format_url()

    def _format_url(self) -> str:
        year = self.aoc_date.year
        day = self.aoc_date.day
        return f"{self.BASE_URL}/{year}/day/{day}/input"

    def check_local(self) -> bool:
        if self.input_path.exists():
            self.logger.info(f"Local input file found at {self.input_path}")
            return True
        else:
            self.logger.info(f"Local input file not found at {self.input_path}")
            return False

    def get_input_path(self) -> Path:
        input_cfg = self.config.config.get("inputs", {})
        base_path = input_cfg.get("path", str(self.DEFAULT_PATH))
        file_str = input_cfg.get("format", "{year}/input_{year}_day_{day:02d}.txt")
        rel_path = file_str.format(year=self.aoc_date.year, day=self.aoc_date.day)
        full_path = Path(base_path).expanduser().joinpath(rel_path)
        return full_path

    def fetch_input(self) -> str:
        session = AoCSession(self.config)
        response = session.get(self.url)
        if response.status_code == 200:
            self.logger.info(
                f"Fetched input for {self.aoc_date.year} Day {self.aoc_date.day:02d}"
            )
            return response.text
        else:
            self.logger.warning(f"Failed to fetch input: {response.status_code}")
            return ""

    def read_local(self) -> str:
        try:
            with self.input_path.open("r") as file:
                return file.read()
        except FileNotFoundError:
            self.logger.error(f"File not found: {self.input_path}")
            return ""

    def write_input(self, overwrite: bool = False) -> None:
        if self.check_local():
            if not overwrite:
                self.logger.info(
                    "Local file exists. Skipping write (use overwrite=True to force)."
                )
                return
            else:
                self.logger.info("Overwriting existing input file.")

        self.input_path.parent.mkdir(parents=True, exist_ok=True)
        input_data = self.fetch_input()
        if input_data:
            with self.input_path.open("w") as file:
                file.write(input_data.strip())
            self.logger.info(f"Input written to {self.input_path}")

    def get_or_fetch(self) -> str:
        if self.check_local():
            return self.read_local()

        self.logger.info("Fetching input because it was not found locally.")
        self.write_input(overwrite=False)
        return self.read_local()
