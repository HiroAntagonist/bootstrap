# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Bootstrap CLI is a scaffolding tool for creating production-ready SaaS applications as monorepos. It uses Copier/Jinja2 templating to generate projects supporting Python (FastAPI) or Go (net/http) backends with deployment configurations for Fly.io or Kubernetes.

## Commands

```bash
task setup          # Install dependencies (runs uv sync)
task test           # Run all tests (uv run pytest tests/)
task lint           # Lint and format (ruff check/format + mypy)
task run -- <args>  # Run the CLI (uv run bootstrap <args>)

# Run a single test
uv run pytest tests/e2e/test_generation.py::test_init_python_project -v

# Run CLI directly during development
uv run bootstrap init my-project --backend python
uv run bootstrap doctor
uv run bootstrap add package my-lib --type python
```

## Architecture

### CLI Structure
- **Entry point**: `src/bootstrap/cli.py` - Typer app with subcommands registered from `commands/` modules
- **Commands**: `init.py` (project creation), `add.py` (component addition), `doctor.py` (environment check)

### Template System
Templates live in `src/bootstrap/templates/`:
- `monorepo/` - Base project structure (Taskfile, pyproject.toml, infra/, api/, ops/)
- `backend-python/` - FastAPI service scaffold
- `backend-go/` - Go net/http service scaffold
- `package-python/`, `package-go/` - Shared library templates

Each template has a `copier.yaml` defining variables. The init command runs Copier twice: first for monorepo base, then for the selected backend into `services/`.

### Generated Project Layout
```
<project>/
├── services/      # Backend microservices
├── apps/          # Client applications (CLI, web, mobile)
├── packages/      # Shared libraries (language-specific)
├── infra/         # Docker, Fly.toml deployment configs
├── api/           # OpenAPI specifications
└── ops/           # Operational runbooks
```

### Key Patterns
- **Two-phase scaffolding**: `init` runs monorepo template first, then backend template into `services/`
- **Polyglot workspaces**: Python uses uv workspaces (`tool.uv.workspace` in pyproject.toml), Go uses standard modules
- **OpenAPI-driven**: Generated projects include API client generation from specs

## Testing

Tests use pytest with fixtures defined in `tests/conftest.py`:
- `runner` - Typer CliRunner for invoking commands
- `temp_workspace` - Temporary directory that becomes cwd during test

E2E tests in `tests/e2e/test_generation.py` validate full project scaffolding by invoking `bootstrap init` and checking generated file structure.

## Required External Tools

The generated projects (not this CLI) require: `uv`, `task`, `docker`, `go` (for Go backends), `gh` (for remote repo creation).
