import shutil
import typer
from rich.console import Console
from rich.table import Table

console = Console()

REQUIRED_TOOLS = [
    ("uv", "Python package manager (https://astral.sh/uv)"),
    ("go", "Go programming language (https://go.dev)"),
    ("task", "Task runner (https://taskfile.dev)"),
    ("docker", "Container runtime"),
    ("gh", "GitHub CLI (https://cli.github.com)"),
]

def check_tools():
    """Check if all required tools are installed."""
    console.print("[bold]Checking environment...[/bold]")
    
    table = Table(title="Tool Status")
    table.add_column("Tool", style="cyan")
    table.add_column("Status", style="bold")
    table.add_column("Path", style="dim")
    
    all_ok = True
    
    for tool, desc in REQUIRED_TOOLS:
        path = shutil.which(tool)
        if path:
            status = "[green]OK[/green]"
            path_str = path
        else:
            status = "[red]MISSING[/red]"
            path_str = f"Install from: {desc}"
            all_ok = False
            
        table.add_row(tool, status, path_str)
        
    console.print(table)
    
    if not all_ok:
        console.print("\n[red]Some tools are missing. Please install them to ensure full functionality.[/red]")
        raise typer.Exit(code=1)
    else:
        console.print("\n[green]All systems normal. You are ready to bootstrap![/green]")
