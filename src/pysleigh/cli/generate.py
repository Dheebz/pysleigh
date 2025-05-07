import typer
from pysleigh.modules.generate_solution import AoCSolutionGenerator
from pysleigh.modules.generate_test import AoCTestGenerator
from pysleigh.utilities.date import AoCDate

generate_app = typer.Typer()


@generate_app.command("solution")
def generate_solution(
    year: int = typer.Option(
        None, help="Year of the puzzle (default: latest available)"
    ),
    day: int = typer.Option(None, help="Day of the puzzle (default: latest available)"),
    overwrite: bool = typer.Option(
        False, "--overwrite", help="Overwrite existing solution file"
    ),
    show: bool = typer.Option(
        False, "--show", help="Print the generated solution to stdout"
    ),
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

        generator = AoCSolutionGenerator(aoc_date=date)
        generator.write_solution(overwrite=overwrite)
        typer.secho(
            f"Solution file created at {generator.solution_path}", fg=typer.colors.GREEN
        )

        if show:
            typer.echo(generator.solution_path.read_text())

    except Exception as e:
        typer.secho(f"[Error] {e}", fg=typer.colors.RED)


@generate_app.command("test")
def generate_test(
    year: int = typer.Option(
        None, help="Year of the puzzle (default: latest available)"
    ),
    day: int = typer.Option(None, help="Day of the puzzle (default: latest available)"),
    overwrite: bool = typer.Option(
        False, "--overwrite", help="Overwrite existing test file"
    ),
    show: bool = typer.Option(
        False, "--show", help="Print the generated test to stdout"
    ),
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

        generator = AoCTestGenerator(aoc_date=date)
        generator.write_test(overwrite=overwrite)

        if show and generator.test_path.exists():
            typer.echo(generator.test_path.read_text())

        if generator.test_path.exists():
            typer.secho(
                f"Test file generated at {generator.test_path}", fg=typer.colors.GREEN
            )
        else:
            typer.secho(
                f"Test file not found at {generator.test_path}", fg=typer.colors.RED
            )
    except Exception as e:
        typer.secho(f"[Error] {e}", fg=typer.colors.RED)
