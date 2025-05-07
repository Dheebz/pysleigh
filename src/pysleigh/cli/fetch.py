import typer
from pysleigh.modules.input import AoCInput
from pysleigh.modules.article import AoCArticle
from pysleigh.modules.answers import AoCAnswers
from pysleigh.utilities.date import AoCDate

fetch_app = typer.Typer()


@fetch_app.command("input")
def fetch_input(
    year: int = typer.Option(
        None, help="Year of the puzzle (default: latest available)"
    ),
    day: int = typer.Option(None, help="Day of the puzzle (default: latest available)"),
    overwrite: bool = typer.Option(
        False, "--overwrite", help="Force re-download of the input file"
    ),
    show: bool = typer.Option(False, "--show", help="Print the puzzle input to stdout"),
):
    try:
        if year is not None and day is not None:
            date = AoCDate(year, day)
        elif year is None and day is None:
            date = AoCDate(*AoCDate._compute_max_date())
        elif year is None:
            date = AoCDate(AoCDate._compute_max_date()[0], day)
        elif day is None:
            date = AoCDate(year, AoCDate._compute_max_date()[1])

        aoc_input = AoCInput(aoc_date=date)
        aoc_input.write_input(overwrite=overwrite)
        typer.secho(f"Input available at {aoc_input.input_path}", fg=typer.colors.GREEN)
        if show:
            typer.echo("\n" + aoc_input.read_local())

    except Exception as e:
        typer.secho(f"[Error] {e}", fg=typer.colors.RED)


@fetch_app.command("article")
def fetch_article(
    year: int = typer.Option(
        None, help="Year of the puzzle (default: latest available)"
    ),
    day: int = typer.Option(None, help="Day of the puzzle (default: latest available)"),
    overwrite: bool = typer.Option(
        False, "--overwrite", help="Force re-download of the article file"
    ),
    show: bool = typer.Option(
        False, "--show", help="Print the puzzle article to stdout"
    ),
):
    from pysleigh.utilities.date import AoCDate

    try:
        if year is not None and day is not None:
            date = AoCDate(year, day)
        elif year is None and day is None:
            date = AoCDate(*AoCDate._compute_max_date())
        elif year is None:
            date = AoCDate(AoCDate._compute_max_date()[0], day)
        elif day is None:
            date = AoCDate(year, AoCDate._compute_max_date()[1])

        article = AoCArticle(aoc_date=date)
        article.write_article(overwrite=overwrite)
        typer.secho(
            f"Article available at {article.article_path}", fg=typer.colors.GREEN
        )
        if show:
            typer.echo("\n" + article.read_local())

    except Exception as e:
        typer.secho(f"[Error] {e}", fg=typer.colors.RED)


@fetch_app.command("answer")
def fetch_answers(
    year: int = typer.Option(
        None, help="Year of the puzzle (default: latest available)"
    ),
    day: int = typer.Option(None, help="Day of the puzzle (default: latest available)"),
    overwrite: bool = typer.Option(
        False, "--overwrite", help="Force re-download of the answers file"
    ),
    show: bool = typer.Option(False, "--show", help="Print the answers to stdout"),
):
    try:
        if year is not None and day is not None:
            date = AoCDate(year, day)
        elif year is None and day is None:
            date = AoCDate(*AoCDate._compute_max_date())
        elif year is None:
            date = AoCDate(AoCDate._compute_max_date()[0], day)
        elif day is None:
            date = AoCDate(year, AoCDate._compute_max_date()[1])

        answers = AoCAnswers(aoc_date=date)
        result = answers.get_or_fetch()
        answers.write_answers(result, overwrite=overwrite)

        typer.secho(
            f"Answers file available at {answers.answers_path}", fg=typer.colors.GREEN
        )
        if show:
            typer.echo(
                f"\nPart 1: {result.get('part1')}\nPart 2: {result.get('part2')}"
            )

    except Exception as e:
        typer.secho(f"[Error] {e}", fg=typer.colors.RED)
