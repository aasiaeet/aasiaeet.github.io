#!/bin/bash
# Update publications from Zotero export
#
# Usage: ./scripts/update_publications.sh
#
# Prerequisites:
# 1. Export your Zotero collection to site/mypapers/
#    - In Zotero: Right-click collection → Export Collection
#    - Format: BibTeX
#    - Check "Export Files"
#    - Save as site/mypapers/mypapers.bib
#
# This script will:
# 1. Import from Zotero (copy PDFs, generate clean BibTeX, suggest topics)
# 2. Convert BibTeX to JSON for Hugo

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"

echo "=== Updating Publications from Zotero ==="
echo ""

# Step 1: Import from Zotero
echo "Step 1: Importing from Zotero..."
python3 "$SCRIPT_DIR/import_zotero.py"

# Step 2: Convert BibTeX to JSON
echo ""
echo "Step 2: Converting BibTeX to JSON..."
python3 "$SCRIPT_DIR/bib2json.py" \
    "$ROOT_DIR/site/bib/publications.bib" \
    "$ROOT_DIR/site/data/publications.json" \
    "$ROOT_DIR/site/data/pub_topics.yaml"

echo ""
echo "=== Publications Updated ==="
echo ""
echo "Next steps:"
echo "1. Review site/data/pub_topics.yaml for topic accuracy"
echo "2. Run ./scripts/build.sh to rebuild the site"
echo "   (or just 'hugo' in site/ for quick preview)"
echo ""
