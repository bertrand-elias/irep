import importlib.metadata

import typer

app = typer.Typer(help="Interactive Review & Evidence Pipeline CLI")

def version_callback(value: bool) -> None:
    if value:
        version = importlib.metadata.version("irep")
        typer.echo(f"irep {version}")
        raise typer.Exit()

@app.callback()
def main(
    version: bool | None = typer.Option(
        None,
        "--version",
        "-v",
        help="Show application version and exit.",
        callback=version_callback,
        is_eager=True,
    ),
) -> None:
    """Interactive Review & Evidence Pipeline entrypoint."""

    
if __name__ == "__main__":
    app()