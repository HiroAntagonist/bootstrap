#!/bin/bash
set -eo pipefail

echo "🚀 Installing Bootstrap CLI..."

# Check requirements
if ! command -v uv &> /dev/null; then
    echo "❌ 'uv' is not installed. Please install it first: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Install/Sync dependencies
echo "📦 Syncing dependencies..."
uv sync

# Link to local bin (assuming ~/.local/bin exists and is in PATH, or standard user bin)
# For simplicity in this dev environment, we'll just output the alias command or try to link if possible.
# A robust install might use `uv tool install .` if available or `pipx`.

# Using 'uv tool' is the modern way if available, else standard pip install
if uv tool --help &> /dev/null; then
    echo "🔧 Installing as a tool via uv..."
    uv tool install . --force
else
    echo "⚠️ 'uv tool' not available. You can run the tool using:"
    echo "   uv run bootstrap"
fi

echo "✅ Installation complete!"
