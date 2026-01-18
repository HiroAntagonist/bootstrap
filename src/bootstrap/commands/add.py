import typer
from rich.console import Console
from pathlib import Path
import copier

console = Console()
app = typer.Typer(help="Add components to the project.")

@app.command("package")
def add_package(
    name: str = typer.Argument(..., help="Name of the package to add"),
    type: str = typer.Option("python", "--type", "-t", help="Package type (python or go)"),
):
    """Add a new shared package."""
    root_dir = Path.cwd()
    # Basic check to see if we are in a project root
    if not (root_dir / "pyproject.toml").exists() and not (root_dir / "taskfile.yml").exists():  # loose check
         console.print("[yellow]Warning: Could not detect project root (no pyproject.toml or taskfile.yml found).[/yellow]")
    
    packages_dir = root_dir / "packages"
    packages_dir.mkdir(exist_ok=True)
    
    package_path = packages_dir / name
    if package_path.exists():
        console.print(f"[red]Error: Package directory '{name}' already exists in packages/.[/red]")
        raise typer.Exit(code=1)

    templates_dir = Path(__file__).parent.parent / "templates"
    template_name = f"package-{type}"
    template_path = templates_dir / template_name
    
    if not template_path.exists():
        console.print(f"[red]Error: Template for package type '{type}' not found.[/red]")
        raise typer.Exit(code=1)

    console.print(f"[bold]Adding {type} package: {name}[/bold]")
    
    data = {"package_name": name}
    
    copier.run_copy(
        src_path=str(template_path),
        dst_path=str(package_path),
        data=data,
        unsafe=True
    )
    
    console.print(f"[green]Package '{name}' created successfully in packages/{name}[/green]")

@app.command("component") # Renaming the old 'add' command logic roughly to 'component' or keeping it? 
# The user request was "bootstrap add package". The old command was "bootstrap add <component>".
# To keep backward compat or just support the old style, we can have a default callback or another command?
# "bootstrap add web" vs "bootstrap add package mypkg"
# The request was specifically for "bootstrap add package".
def add_component(
    component: str = typer.Argument(..., help="Component to add (e.g., 'web', 'ios')"),
):
    """Add a new component (app/service)."""
    # ... existing logic ...
    console.print(f"[bold]Adding component: {component}[/bold]")
    if component in ["web", "ios"]:
        console.print(f"[yellow]Stub: The '{component}' template is not yet implemented.[/yellow]")
    else:
        console.print(f"[red]Unknown component '{component}'. Available: web, ios[/red]")
        raise typer.Exit(code=1)
