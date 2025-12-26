#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Starting Quartz development server ==="
echo "Notes will be available at http://localhost:8080"
echo ""
cd "$ROOT_DIR/quartz"
npx quartz build --serve
