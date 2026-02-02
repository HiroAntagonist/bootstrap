import os
from pathlib import Path
from bootstrap.cli import app

def test_init_python_project(runner, temp_workspace):
    """Test initializing a Python project."""
    result = runner.invoke(app, ["init", "my-py-app", "--backend", "python"])

    assert result.exit_code == 0, result.stdout

    project_root = temp_workspace / "my-py-app"
    assert project_root.exists()
    assert (project_root / "pyproject.toml").exists()
    assert (project_root / "Taskfile.yml").exists()
    assert (project_root / "services/backend/src/backend/main.py").exists()
    assert (project_root / "apps/cli/src/cli/main.py").exists()
    assert (project_root / "packages/my_py_app_api").exists()
    assert (project_root / ".gitignore").exists()

def test_init_go_project(runner, temp_workspace):
    """Test initializing a Go project."""
    result = runner.invoke(app, ["init", "my-go-app", "--backend", "go"])

    assert result.exit_code == 0, result.stdout

    project_root = temp_workspace / "my-go-app"
    assert project_root.exists()
    assert (project_root / "pyproject.toml").exists()  # CLI requires this
    assert (project_root / "services/backend/main.go").exists()
    assert (project_root / "services/backend/Taskfile.yml").exists()
    assert (project_root / "services/backend/go.mod").exists()
    assert (project_root / "Taskfile.yml").exists()
    assert (project_root / "packages/my_go_app_api").exists()

def test_init_existing_directory_fails(runner, temp_workspace):
    """Test failure when directory exists."""
    (temp_workspace / "duplicate").mkdir()
    result = runner.invoke(app, ["init", "duplicate", "--backend", "python"])
    
    assert result.exit_code == 1
    assert "already exists" in result.stdout
