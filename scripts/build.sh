#!/bin/bash
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

# Use local Node 22 if available (for local dev), otherwise use system node
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

echo "=== Converting BibTeX to JSON ==="
python3 "$SCRIPT_DIR/bib2json.py" "$ROOT_DIR/site/bib/publications.bib" "$ROOT_DIR/site/data/publications.json" "$ROOT_DIR/site/data/pub_topics.yaml"

echo "=== Building Quartz notes ==="
cd "$ROOT_DIR/quartz"
npx quartz build

echo "=== Copying Quartz output to Hugo static/notes ==="
rm -rf "$ROOT_DIR/site/static/notes"
cp -r "$ROOT_DIR/quartz/public" "$ROOT_DIR/site/static/notes"

echo "=== Building Hugo site ==="
cd "$ROOT_DIR/site"
hugo --gc --minify

echo "=== Build complete ==="
echo "Output is in: $ROOT_DIR/site/public"
