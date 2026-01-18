import typer
from rich.console import Console
from bootstrap.commands import doctor, init, add

app = typer.Typer(
    name="bootstrap",
    help="SaaS Scaffolding Tool",
    add_completion=False,
    no_args_is_help=True,
)
console = Console()

# Register subcommands
app.command(name="doctor")(doctor.check_tools)
app.command(name="init")(init.init_project)
app.add_typer(add.app, name="add")

def main():
    """Entry point for the CLI."""
    app()

@app.command()
def version():
    """Show version."""
    console.print("Bootstrap CLI v0.1.0")

if __name__ == "__main__":
    main()
