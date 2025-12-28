# Bootstrap CLI

A powerful scaffolding tool for creating production-ready SaaS applications.

## Features
- **Monorepo Support**: Unified structure for Backend, Infra, and Shared Packages.
- **Dual Stack**: Support for Python (FastAPI) and Go (net/http).
- **Production Ready**: Includes CI/CD, Infrastructure (Fly/Docker), and Observability hooks.
- **Extensible**: Add components (`web`, `ios`) as you grow.

## Installation

```bash
./install.sh
```

## Usage

### Initialize a new project
```bash
bootstrap init my-saas --backend python
# OR
bootstrap init my-saas --backend go
```

### Check environment
```bash
bootstrap doctor
```

### Add a component
```bash
bootstrap add web
```

## Development

1. Install `uv` (https://github.com/astral-sh/uv).
2. Sync dependencies:
   ```bash
   uv sync
   ```
3. Run locally:
   ```bash
   uv run bootstrap --help
   ```
