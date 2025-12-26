#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Use local Node 22 and Hugo if available
if [ -d "$HOME/bin/bin" ]; then
    export PATH="$HOME/bin/bin:$HOME/bin:$PATH"
fi

# Check Node version
NODE_VERSION=$(node -v | cut -d'.' -f1 | tr -d 'v')
if [ "$NODE_VERSION" -lt 22 ]; then
    echo "Error: Node 22+ required. You have $(node -v)"
    echo ""
    echo "Install Node 22 with:"
    echo "  curl -fsSL https://nodejs.org/dist/v22.12.0/node-v22.12.0-linux-x64.tar.xz | tar xJ -C ~/bin --strip-components=1"
    echo "  export PATH=\$HOME/bin/bin:\$PATH"
    exit 1
fi

echo "=== Building Quartz notes (one-time) ==="
cd "$ROOT_DIR/quartz"
npx quartz build

echo "=== Copying Quartz output to Hugo static/notes ==="
rm -rf "$ROOT_DIR/site/static/notes"
cp -r "$ROOT_DIR/quartz/public" "$ROOT_DIR/site/static/notes"

echo "=== Starting Hugo development server ==="
echo "Site will be available at http://localhost:1313"
echo ""
echo "Note: For Quartz changes, run 'npx quartz build' in quartz/ directory"
echo "      and copy output to site/static/notes"
echo ""
cd "$ROOT_DIR/site"
hugo server -D --bind 0.0.0.0
