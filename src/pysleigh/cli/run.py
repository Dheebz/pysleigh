import typer
from pysleigh.modules.run_solution import AoCRunner
from pysleigh.modules.run_test import AoCTestRunner
from pysleigh.utilities.date import AoCDate

run_app = typer.Typer()


@run_app.command("solution")
def run_solution(
    year: int = typer.Option(
        None, help="Year of the puzzle (default: latest available)"
    ),
    day: int = typer.Option(None, help="Day of the puzzle (default: latest available)"),
    test: bool = typer.Option(False, "--test", help="Also run tests after solution"),
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

        runner = AoCRunner(aoc_date=date)
        results = runner.run_solution()

        if results:
            typer.secho(
                f"Part 1: {results['part1']} (took {results['time_part1']:.6f}s)",
                fg=typer.colors.GREEN,
            )
            typer.secho(
                f"Part 2: {results['part2']} (took {results['time_part2']:.6f}s)",
                fg=typer.colors.GREEN,
            )

        if test:
            passed = runner.run_tests()
            if passed:
                typer.secho("✅ Tests passed.", fg=typer.colors.BLUE)
            else:
                typer.secho("❌ Some tests failed.", fg=typer.colors.RED)

    except Exception as e:
        typer.secho(f"[Error] {e}", fg=typer.colors.RED)





@run_app.command("test")
def run_test(
    year: int = typer.Option(None, help="Year of the puzzle"),
    day: int = typer.Option(None, help="Day of the puzzle"),
):
    try:
        if year and day:
            aoc_date = AoCDate(year, day)
            runner = AoCTestRunner(aoc_date)
            passed = runner.run_specific_test()
        elif year:
            runner = AoCTestRunner()
            passed = runner.run_year_tests(year)
        else:
            runner = AoCTestRunner()
            passed = runner.run_all_tests()

        if passed:
            typer.secho("✅ Tests passed.", fg=typer.colors.BLUE)
        else:
            typer.secho("❌ Some tests failed.", fg=typer.colors.RED)

    except Exception as e:
        typer.secho(f"[Error] {e}", fg=typer.colors.RED)
