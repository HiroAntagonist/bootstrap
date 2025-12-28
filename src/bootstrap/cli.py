import typer
from typing import Optional
from rich.console import Console

app = typer.Typer(
    name="bootstrap",
    help="SaaS Scaffolding Tool",
    add_completion=False,
    no_args_is_help=True,
)
console = Console()

def main():
    """Entry point for the CLI."""
    app()

@app.command()
def version():
    """Show version."""
    console.print("Bootstrap CLI v0.1.0")

if __name__ == "__main__":
    main()
