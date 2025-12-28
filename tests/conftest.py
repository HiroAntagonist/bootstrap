import pytest
import shutil
import os
from pathlib import Path
from typer.testing import CliRunner
from bootstrap.cli import app

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def temp_workspace(tmp_path):
    """Create a temporary workspace for test execution."""
    current = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(current)
