import typer
from rich.console import Console

console = Console()

def add_component(
    component: str = typer.Argument(..., help="Component to add (e.g., 'web', 'ios')"),
):
    """Add a new component to the existing project."""
    console.print(f"[bold]Adding component: {component}[/bold]")
    
    if component in ["web", "ios"]:
        console.print(f"[yellow]Stub: The '{component}' template is not yet implemented.[/yellow]")
    else:
        console.print(f"[red]Unknown component '{component}'. Available: web, ios[/red]")
        raise typer.Exit(code=1)
