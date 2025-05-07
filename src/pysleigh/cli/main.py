import typer
from pysleigh.cli.fetch import fetch_app
from pysleigh.cli.generate import generate_app
from pysleigh.cli.run import run_app
from pysleigh.cli.benchmark import benchmark_app
from pysleigh.cli.submit import submit_app
from pysleigh.cli.prep import prep_app

app = typer.Typer()
app.add_typer(benchmark_app, name="benchmark")
app.add_typer(fetch_app, name="fetch")
app.add_typer(generate_app, name="generate")
app.add_typer(prep_app, name="prep")
app.add_typer(run_app, name="run")
app.add_typer(submit_app, name="submit")

main = app  # Exported for CLI entrypoint
if __name__ == "__main__":
    app()
