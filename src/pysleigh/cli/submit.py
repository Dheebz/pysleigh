import typer
from pysleigh.modules.submit_solution import AoCSubmitter
from pysleigh.utilities.date import AoCDate

submit_app = typer.Typer(help="Submit AoC puzzle answers.")


@submit_app.command("answer")
def submit_answer(
    year: int = typer.Option(..., help="Year of the puzzle"),
    day: int = typer.Option(..., help="Day of the puzzle"),
    part: int = typer.Option(..., help="Part to submit (1 or 2)"),
    answer: str = typer.Option(
        None, help="Answer to submit. If omitted, will compute."
    ),
    show: bool = typer.Option(False, "--show", help="Print the full HTML response"),
):
    try:
        date = AoCDate(year, day)
        submitter = AoCSubmitter(date)
        ans = answer or submitter.compute_answer(part)
        typer.secho(f"Submitting part {part} answer: {ans}", fg=typer.colors.YELLOW)

        response_html = submitter.submit(part, ans)
        status, summary = submitter.parse_response(response_html)

        color = {
            "correct": typer.colors.GREEN,
            "incorrect": typer.colors.RED,
            "already_submitted": typer.colors.YELLOW,
            "cooldown": typer.colors.MAGENTA,
        }.get(status, typer.colors.WHITE)

        typer.secho(f"[{status.upper()}] {summary}", fg=color)

        if show:
            typer.echo("\n" + response_html)

    except Exception as e:
        typer.secho(f"[Error] {e}", fg=typer.colors.RED)
