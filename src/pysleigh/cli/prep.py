import typer
from pysleigh.utilities.date import AoCDate
from pysleigh.modules.article import AoCArticle
from pysleigh.modules.input import AoCInput
from pysleigh.modules.generate_solution import AoCSolutionGenerator

prep_app = typer.Typer(
    help="Prep your workspace by fetching input, article, and generating solution."
)


@prep_app.command("solution")
def prep_solution(
    year: int = typer.Option(..., help="Year of the puzzle"),
    day: int = typer.Option(
        None, help="Day of the puzzle. If omitted, prep all 25 days."
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", help="Overwrite existing files"
    ),
):
    if day:
        _prep_day(year, day, overwrite)
    else:
        for d in range(1, 26):
            _prep_day(year, d, overwrite)


def _prep_day(year: int, day: int, overwrite: bool):
    try:
        date = AoCDate(year, day)
        typer.secho(f"🔧 Preparing Day {day:02d}, {year}", fg=typer.colors.CYAN)

        article = AoCArticle(date)
        article.write_article(overwrite=overwrite)

        input_obj = AoCInput(date)
        input_obj.write_input(overwrite=overwrite)

        generator = AoCSolutionGenerator(date)
        generator.write_solution(overwrite=overwrite)

        typer.secho(f"✅ Ready: {year}-Day{day:02d}", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(f"[Error] Failed to prep Day {day:02d}: {e}", fg=typer.colors.RED)


from pysleigh.modules.answers import AoCAnswers
from pysleigh.modules.generate_test import AoCTestGenerator


@prep_app.command("test")
def prep_test(
    year: int = typer.Option(..., help="Year of the puzzle"),
    day: int = typer.Option(
        None, help="Day of the puzzle. If omitted, prep all 25 days."
    ),
    overwrite: bool = typer.Option(
        False, "--overwrite", help="Overwrite existing files"
    ),
):
    if day:
        _prep_test_day(year, day, overwrite)
    else:
        for d in range(1, 26):
            _prep_test_day(year, d, overwrite)


def _prep_test_day(year: int, day: int, overwrite: bool):
    try:
        date = AoCDate(year, day)
        typer.secho(
            f"🧪 Preparing test for Day {day:02d}, {year}", fg=typer.colors.BLUE
        )

        answers = AoCAnswers(date)
        answers.get_or_fetch()

        test_gen = AoCTestGenerator(date)
        test_gen.write_test(overwrite=overwrite)

        typer.secho(f"✅ Test ready: {year}-Day{day:02d}", fg=typer.colors.GREEN)
    except Exception as e:
        typer.secho(
            f"[Error] Failed to prep test for Day {day:02d}: {e}", fg=typer.colors.RED
        )
