#!/usr/bin/env bash
# Idempotent repository bootstrap for the Enterprise Agent Platform.
# System packages (Python 3.14, PostgreSQL 16) live in the base snapshot;
# this script only refreshes the project's Python dependencies.
set -euo pipefail

cd "$(dirname "$0")/.."

PYTHON="python3.14"
if ! command -v "$PYTHON" >/dev/null 2>&1; then
  PYTHON="python3"
fi

if [ ! -x ".venv/bin/python" ]; then
  "$PYTHON" -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

python -m pip install --upgrade pip
pip install -r requirements.txt
# ruff is the linter used by the CI "critical errors" check.
pip install ruff

echo "install.sh complete: dependencies ready in .venv ($("$PYTHON" --version))"
