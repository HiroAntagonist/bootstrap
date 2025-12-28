import typer
from typing import Optional
from enum import Enum
from pathlib import Path
from rich.console import Console
import copier

console = Console()

class Backend(str, Enum):
    PYTHON = "python"
    GO = "go"

class Deploy(str, Enum):
    FLY = "fly"
    K8S = "k8s"

def init_project(
    project_name: str = typer.Argument(..., help="Name of the project directory to create"),
    backend: Backend = typer.Option(..., "--backend", "-b", help="Backend language choice"),
    deploy: Deploy = typer.Option(Deploy.FLY, "--deploy", "-d", help="Deployment target"),
    create_remote: bool = typer.Option(False, "--remote", help="Create a GitHub remote repository"),
    private_remote: bool = typer.Option(True, "--private/--public", help="Visibility of the remote repository"),
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing directory"),
):
    """Initialize a new SaaS project."""
    project_path = Path(project_name).resolve()
    
    # Resolve templates directory (assumes templates are in src/bootstrap/templates)
    # __file__ is src/bootstrap/commands/init.py
    # Templates are at src/bootstrap/templates
    templates_dir = Path(__file__).parent.parent / "templates"
    
    if not templates_dir.exists():
        console.print(f"[red]Error: Templates directory not found at {templates_dir}[/red]")
        raise typer.Exit(code=1)

    console.print(f"[bold]Initializing project: {project_name}[/bold]")
    console.print(f"Backend: [cyan]{backend.value}[/cyan]")
    console.print(f"Deploy: [cyan]{deploy.value}[/cyan]")
    
    # Check if directory exists
    if project_path.exists():
        if not force:
            console.print(f"[red]Error: Directory '{project_name}' already exists.[/red]")
            console.print("Use [bold]--force[/bold] to overwrite.")
            raise typer.Exit(code=1)
        else:
            console.print(f"[yellow]Warning: Overwriting existing directory '{project_name}'[/yellow]")
    
    # Common Data for Templates
    data = {
        "project_name": project_name,
        "backend_type": backend.value,
        "deploy_target": deploy.value,
    }

    # 1. Monorepo Base
    console.print("[dim]Step 1: Scaffolding Monorepo...[/dim]")
    copier.run_copy(
        src_path=str(templates_dir / "monorepo"),
        dst_path=str(project_path),
        data=data,
        overwrite=True, # We handled the top-level check
        unsafe=True # Local template
    )
    
    # 2. Backend
    console.print(f"[dim]Step 2: Scaffolding {backend.value} Backend...[/dim]")
    backend_template = templates_dir / f"backend-{backend.value}"
    if backend_template.exists():
        copier.run_copy(
            src_path=str(backend_template),
            dst_path=str(project_path),
            data=data,
            overwrite=True,
            unsafe=True
        )
    else:
        console.print(f"[yellow]Warning: Backend template for {backend.value} not found, skipping...[/yellow]")

    # 3. Rename CLI script if needed or post-processing
    # The monorepo template creates `cli/main.py`.
    # We might want to rename or ensure permissions.
    
    # 4. Git Init & Remote
    console.print("[dim]Step 3: Initializing Git...[/dim]")
    try:
        if not (project_path / ".git").exists():
            # Use sh or subprocess
            import subprocess
            subprocess.run(["git", "init"], cwd=project_path, check=True, stdout=subprocess.DEVNULL)
            subprocess.run(["git", "add", "."], cwd=project_path, check=True, stdout=subprocess.DEVNULL)
            subprocess.run(["git", "commit", "-m", "Initial commit from bootstrap"], cwd=project_path, check=True, stdout=subprocess.DEVNULL)
            
            if create_remote:
                vis_flag = "--private" if private_remote else "--public"
                console.print(f"[dim]Step 4: Creating {vis_flag.replace('--','')} GitHub remote...[/dim]")
                # Requres gh cli
                try:
                    subprocess.run(["gh", "repo", "create", project_name, vis_flag, "--source=.", "--remote=origin", "--push"], cwd=project_path, check=True)
                except subprocess.CalledProcessError:
                    console.print("[red]Failed to create GitHub remote. Is 'gh' installed and authenticated?[/red]")
    except Exception as e:
        console.print(f"[yellow]Git initialization failed: {e}[/yellow]")

    console.print("\n[green]🚀 Project initialized successfully![/green]")
    console.print("\nNext Steps:")
    console.print(f"  cd {project_name}")
    console.print("  task setup")
    console.print("  task dev")
