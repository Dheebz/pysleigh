import typer
from pysleigh.utilities.date import AoCDate
from pysleigh.modules.benchmark import AoCBenchmark

benchmark_app = typer.Typer(help="Benchmark AoC solutions.")


@benchmark_app.command("solution")
@benchmark_app.command("solution")
def benchmark_solution(
    year: int = typer.Option(None, help="Year of the puzzle"),
    day: int = typer.Option(None, help="Day of the puzzle"),
    runs: int = typer.Option(5, help="Number of times to run the benchmark."),
):

    aoc_date = AoCDate(year, day) if year and day else None
    benchmark = AoCBenchmark(aoc_date, runs=runs)

    if year and day:
        result = benchmark.benchmark_day(year, day)
        if result:
            typer.secho(
                f"{year}-Day{day:02d} ✓ avg1: {result['avg_part1']:.6f}s, avg2: {result['avg_part2']:.6f}s "
                f"over {result['runs']} runs",
                fg=typer.colors.GREEN,
            )
    elif year:
        benchmark.benchmark_year(year)
    else:
        benchmark.benchmark_all()
