import re
from pathlib import Path
from markdownify import markdownify as md
from bs4 import BeautifulSoup

from pysleigh.utilities.config import AoCConfig
from pysleigh.utilities.logger import AoCLogger
from pysleigh.utilities.date import AoCDate
from pysleigh.utilities.session import AoCSession


class AoCArticle:
    logger = AoCLogger().get_logger()
    DEFAULT_PATH = Path("~/Workspace/advent-of-code/articles")

    def __init__(
        self, aoc_date: AoCDate | None = None, config: AoCConfig | None = None
    ):
        self.aoc_date = aoc_date or AoCDate(*AoCDate._compute_max_date())
        self.config = config or AoCConfig()
        self.article_path = self.get_article_path()

        self.url = self._format_url()

    def _format_url(self) -> str:
        year = self.aoc_date.year
        day = self.aoc_date.day
        return f"https://adventofcode.com/{year}/day/{day}"

    def get_article_path(self) -> Path:
        article_cfg = self.config.config.get("articles", {})
        base_path = article_cfg.get("path", str(self.DEFAULT_PATH))
        file_str = article_cfg.get("format", "{year}/article_{year}_day_{day:02d}.md")
        rel_path = file_str.format(year=self.aoc_date.year, day=self.aoc_date.day)
        full_path = Path(base_path).expanduser().joinpath(rel_path)
        return full_path

    def check_local(self) -> bool:
        if self.article_path.exists():
            self.logger.info(f"Local article file found at {self.article_path}")
            return True
        else:
            self.logger.info(f"Local article file not found at {self.article_path}")
            return False

    def fetch_article(self) -> str:
        session = AoCSession(self.config)
        response = session.get(self.url)
        if response.status_code == 200:
            self.logger.info(
                f"Fetched article for {self.aoc_date.year} Day {self.aoc_date.day:02d}"
            )
            html = response.text
            article_content = self.format_article(html)
            return article_content
        else:
            self.logger.warning(f"Failed to fetch article: {response.status_code}")
            return ""

    def format_article(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        title = self.__extract_title(soup)
        header = self.__generate_header(title)
        body = self.__convert_to_markdown(soup)
        return f"{header}\n{body}"

    def __extract_title(self, soup: BeautifulSoup) -> str:
        header = soup.find("h2")
        title_text = header.text.strip()
        title_match = re.search(r"Day\s\d+:\s(.*)", title_text)
        return title_match.group(1) if title_match else title_text

    def __generate_header(self, title: str) -> str:
        title = title.replace("-", "").strip()
        return f"# --- Advent of Code {self.aoc_date.year} - Day {self.aoc_date.day:02d}: {title} ---"

    def __convert_to_markdown(self, soup: BeautifulSoup) -> str:
        articles = soup.find_all("article")
        if not articles:
            self.logger.warning("No articles found in the HTML content.")
            return ""

        markdown_parts = []
        for i, article in enumerate(articles):
            if heading := article.find("h2"):
                heading.decompose()

            part_title = "Part One" if i == 0 else "Part Two"
            markdown = md(str(article), heading_style="ATX")
            markdown_parts.append(f"\n## --- {part_title} ---\n\n{markdown}\n")
        return "\n".join(markdown_parts)

    def read_local(self) -> str:
        try:
            with self.article_path.open("r") as file:
                return file.read()
        except FileNotFoundError:
            self.logger.error(f"File not found: {self.article_path}")
            return ""

    def write_article(self, overwrite: bool = False) -> None:
        if self.check_local():
            if not overwrite:
                self.logger.info(
                    f"Article already exists at {self.article_path}. Use overwrite=True to overwrite."
                )
                return
            else:
                self.logger.info(f"Overwriting existing article at {self.article_path}")

        article_content = self.fetch_article()
        if article_content:
            self.article_path.parent.mkdir(parents=True, exist_ok=True)
            with self.article_path.open("w") as file:
                file.write(article_content)
            self.logger.info(f"Article written to {self.article_path}")
        else:
            self.logger.error("Failed to write article: No content fetched.")

    def get_or_fetch(self) -> str:
        """
        Return the article content. If not found locally, fetch from the website and save.
        """
        if self.check_local():
            return self.read_local()

        self.logger.info("Fetching article because it was not found locally.")
        self.write_article(overwrite=False)
        return self.read_local()
