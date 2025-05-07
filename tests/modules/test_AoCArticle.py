import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path
from pysleigh.modules.article import AoCArticle
from pysleigh.utilities.date import AoCDate


@pytest.mark.unit
class TestAoCArticle:
    def test_get_article_path_uses_config(self, tmp_path):
        cfg = {
            "articles": {
                "path": str(tmp_path),
                "format": "Y{year}/article_{year}_{day}.md",
            }
        }
        a = AoCArticle(AoCDate(2021, 5), config=MagicMock(config=cfg))
        expected = tmp_path / "Y2021" / "article_2021_5.md"
        assert a.get_article_path() == expected

    def test_format_article_converts_html_to_markdown(self):
        html = """
        <article><h2>Day 3: Elves</h2><p>This is part one.</p></article>
        <article><h2>Day 3: Elves</h2><p>This is part two.</p></article>
        """
        a = AoCArticle(AoCDate(2022, 3))
        md = a.format_article(html)
        assert "# --- Advent of Code 2022 - Day 03: Elves ---" in md
        assert "## --- Part One ---" in md
        assert "## --- Part Two ---" in md
        assert "This is part one." in md
        assert "This is part two." in md

    def test_fetch_article_logs_on_failure(self, caplog):
        with patch("pysleigh.utilities.session.AoCSession.get") as mock_get:
            mock_get.return_value.status_code = 404
            a = AoCArticle(AoCDate(2022, 5))
            result = a.fetch_article()
            assert result == ""
            assert "Failed to fetch article" in caplog.text

    def test_get_or_fetch_reads_local_when_exists(self, tmp_path):
        file = tmp_path / "article.md"
        file.write_text("# local content")
        with patch.object(AoCArticle, "get_article_path", return_value=file):
            a = AoCArticle(AoCDate(2022, 1))
            content = a.get_or_fetch()
            assert "# local content" in content
