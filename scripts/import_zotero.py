#!/usr/bin/env python3
"""
Import publications from Zotero export.

This script:
1. Reads mypapers.bib from Zotero export
2. Extracts PDFs from nested folder structure
3. Copies PDFs to site/static/publications/ with proper names
4. Generates clean publications.bib
5. Auto-generates topic suggestions based on titles/abstracts

Usage: python import_zotero.py [--suggest-topics]

The --suggest-topics flag prints topic suggestions that can be reviewed
and added to pub_topics.yaml
"""

import re
import os
import sys
import shutil
import yaml
from pathlib import Path

# Directories
SCRIPT_DIR = Path(__file__).parent.resolve()
ROOT_DIR = SCRIPT_DIR.parent
ZOTERO_DIR = ROOT_DIR / "site" / "mypapers"
ZOTERO_BIB = ZOTERO_DIR / "mypapers.bib"
ZOTERO_FILES = ZOTERO_DIR / "files"
OUTPUT_BIB = ROOT_DIR / "site" / "bib" / "publications.bib"
OUTPUT_PDF_DIR = ROOT_DIR / "site" / "static" / "publications"
TOPICS_FILE = ROOT_DIR / "site" / "data" / "pub_topics.yaml"

# Topic keywords for auto-classification
TOPIC_KEYWORDS = {
    "Computational Biology": [
        "gene", "expression", "transcriptome", "microrna", "mirna", "mir",
        "transcription", "biological", "genome", "genomic", "sequencing",
        "rna", "dna", "protein", "molecular", "cell", "tumor", "cancer",
        "oncogenetic", "intratumor", "heterogeneity"
    ],
    "Cancer Research": [
        "cancer", "tumor", "oncogenetic", "oncology", "carcinoma",
        "malignant", "metastasis", "chemotherapy", "intratumor"
    ],
    "Machine Learning": [
        "learning", "neural", "deep", "model", "estimation", "regression",
        "classification", "optimization", "algorithm", "sparse", "lasso",
        "high-dimensional", "high dimensional", "data enrichment", "multi-task"
    ],
    "Causal Inference": [
        "causal", "treatment effect", "cate", "rct", "randomized",
        "confounding", "dag", "bayesian network", "structure learning"
    ],
    "Social Networks": [
        "social", "network", "influence", "diffusion", "spread",
        "maximization", "graph", "community"
    ],
    "Natural Language Processing": [
        "text", "sentiment", "tweet", "nlp", "language", "word"
    ],
    "Immunology": [
        "immune", "immunity", "immunoediting", "vaccine", "t cell",
        "nk cell", "epitope", "hiv", "checkpoint inhibitor", "sjs", "ten"
    ],
    "Drug Discovery": [
        "drug", "pharmacology", "therapeutic", "treatment", "inhibitor"
    ],
    "Microbiome": [
        "microbiome", "microbiota", "bacteria", "gut", "keystone"
    ],
    "Cybersecurity": [
        "security", "malware", "dns", "cyber", "attack", "detection"
    ],
    "Statistical Methods": [
        "statistical", "bayesian", "inference", "estimator", "hypothesis",
        "variance", "confidence", "p-value", "methodology"
    ],
}


def parse_zotero_bib(filepath):
    """Parse Zotero BibTeX file and return list of entries."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    entries = []

    # Match BibTeX entries
    entry_pattern = r'@(\w+)\s*\{\s*([^,]+)\s*,'

    for match in re.finditer(entry_pattern, content):
        entry_type = match.group(1).lower()
        key = match.group(2).strip()

        # Find matching closing brace
        start = match.end()
        brace_count = 1
        pos = start

        while pos < len(content) and brace_count > 0:
            if content[pos] == '{':
                brace_count += 1
            elif content[pos] == '}':
                brace_count -= 1
            pos += 1

        if brace_count == 0:
            entry_content = content[match.start():pos]
            entry_fields = parse_fields(content[start:pos-1])
            entry_fields['_type'] = entry_type
            entry_fields['_key'] = key
            entry_fields['_raw'] = entry_content
            entries.append(entry_fields)

    return entries


def parse_fields(content):
    """Parse fields from a BibTeX entry."""
    fields = {}

    # Match field = value patterns
    field_pattern = r'(\w+)\s*=\s*'

    for match in re.finditer(field_pattern, content):
        field_name = match.group(1).lower()
        start = match.end()

        # Skip whitespace
        while start < len(content) and content[start] in ' \t\n':
            start += 1

        if start >= len(content):
            continue

        # Determine value delimiter
        if content[start] == '{':
            brace_count = 1
            pos = start + 1
            while pos < len(content) and brace_count > 0:
                if content[pos] == '{':
                    brace_count += 1
                elif content[pos] == '}':
                    brace_count -= 1
                pos += 1
            value = content[start+1:pos-1]
        elif content[start] == '"':
            pos = start + 1
            while pos < len(content) and content[pos] != '"':
                pos += 1
            value = content[start+1:pos]
        else:
            pos = start
            while pos < len(content) and content[pos] not in ',}\n':
                pos += 1
            value = content[start:pos].strip()

        fields[field_name] = value

    return fields


def extract_pdf_path(file_field, zotero_files_dir):
    """Extract PDF path from Zotero file field."""
    if not file_field:
        return None

    # Parse Zotero file field format: "Label:files/123/filename.pdf:application/pdf"
    # Can have multiple files separated by ;
    parts = file_field.split(';')

    for part in parts:
        part = part.strip()
        # Match pattern: anything:files/...:mimetype
        match = re.search(r':?(files/[^:]+\.pdf)', part, re.IGNORECASE)
        if match:
            rel_path = match.group(1)
            # The path is relative to the parent of zotero_files_dir
            full_path = zotero_files_dir.parent / rel_path
            if full_path.exists():
                return full_path

    return None


def copy_pdfs(entries):
    """Copy PDFs from Zotero export to publications folder."""
    OUTPUT_PDF_DIR.mkdir(parents=True, exist_ok=True)

    copied = []
    missing = []

    for entry in entries:
        key = entry['_key']
        file_field = entry.get('file', '')

        pdf_path = extract_pdf_path(file_field, ZOTERO_FILES)

        if pdf_path and pdf_path.exists():
            dest_path = OUTPUT_PDF_DIR / f"{key}.pdf"
            shutil.copy2(pdf_path, dest_path)
            copied.append((key, pdf_path.name))
        else:
            if file_field:
                missing.append((key, file_field))

    return copied, missing


def generate_clean_bib(entries):
    """Generate clean BibTeX file without Zotero-specific fields."""
    # Fields to exclude
    exclude_fields = {'file', 'urldate', 'shorttitle', 'copyright', 'language',
                      'address', 'series', 'isbn', '_type', '_key', '_raw'}

    output_lines = []

    for entry in entries:
        entry_type = entry['_type']
        key = entry['_key']

        output_lines.append(f"@{entry_type}{{{key},")

        for field, value in entry.items():
            if field in exclude_fields:
                continue
            if not value:
                continue

            # Clean up LaTeX commands in value
            clean_value = value.replace('\\textit', '').replace('\\textbf', '')
            clean_value = re.sub(r'\{\\textbackslash\}', '\\\\', clean_value)

            # Format field
            if field in ['year', 'volume', 'number']:
                output_lines.append(f"  {field} = {{{clean_value}}},")
            else:
                output_lines.append(f"  {field} = {{{clean_value}}},")

        output_lines.append("}")
        output_lines.append("")

    return "\n".join(output_lines)


def suggest_topics(entries):
    """Suggest topics for each entry based on title and abstract."""
    suggestions = {}

    for entry in entries:
        key = entry['_key']
        title = entry.get('title', '').lower()
        abstract = entry.get('abstract', '').lower()
        text = title + " " + abstract

        matched_topics = []

        for topic, keywords in TOPIC_KEYWORDS.items():
            for kw in keywords:
                if kw.lower() in text:
                    if topic not in matched_topics:
                        matched_topics.append(topic)
                    break

        # Limit to top 2-3 topics
        if matched_topics:
            suggestions[key] = matched_topics[:3]
        else:
            # Default based on entry type
            if entry['_type'] == 'article':
                suggestions[key] = ['Journal Articles']
            elif entry['_type'] in ['inproceedings', 'conference']:
                suggestions[key] = ['Conference Papers']
            else:
                suggestions[key] = ['Other']

    return suggestions


def update_topics_file(suggestions):
    """Update pub_topics.yaml with new entries."""
    # Load existing topics
    existing = {}
    if TOPICS_FILE.exists():
        with open(TOPICS_FILE, 'r') as f:
            existing = yaml.safe_load(f) or {}

    # Merge - don't overwrite existing manually set topics
    updated = False
    for key, topics in suggestions.items():
        if key not in existing:
            existing[key] = topics
            updated = True

    if updated:
        with open(TOPICS_FILE, 'w') as f:
            yaml.dump(existing, f, default_flow_style=False, sort_keys=True, allow_unicode=True)

    return updated


def main():
    suggest_topics_flag = '--suggest-topics' in sys.argv

    print("=" * 60)
    print("Zotero Import Script")
    print("=" * 60)

    # Check if Zotero export exists
    if not ZOTERO_BIB.exists():
        print(f"ERROR: Zotero export not found at {ZOTERO_BIB}")
        print("Please export your Zotero collection to site/mypapers/")
        sys.exit(1)

    print(f"\n1. Reading Zotero BibTeX from {ZOTERO_BIB}...")
    entries = parse_zotero_bib(ZOTERO_BIB)
    print(f"   Found {len(entries)} entries")

    print(f"\n2. Copying PDFs to {OUTPUT_PDF_DIR}...")
    copied, missing = copy_pdfs(entries)
    print(f"   Copied {len(copied)} PDFs")
    if missing:
        print(f"   Missing/not found: {len(missing)}")
        for key, path in missing[:5]:
            print(f"     - {key}: {path[:50]}...")

    print(f"\n3. Generating clean BibTeX at {OUTPUT_BIB}...")
    clean_bib = generate_clean_bib(entries)
    OUTPUT_BIB.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_BIB, 'w', encoding='utf-8') as f:
        f.write(clean_bib)
    print(f"   Written {len(entries)} entries")

    print(f"\n4. Suggesting topics...")
    suggestions = suggest_topics(entries)

    if suggest_topics_flag:
        print("\n   Topic suggestions (review and add to pub_topics.yaml):")
        print("   " + "-" * 50)
        for key, topics in sorted(suggestions.items()):
            print(f"   {key}:")
            for t in topics:
                print(f"     - {t}")

    print(f"\n5. Updating {TOPICS_FILE}...")
    updated = update_topics_file(suggestions)
    if updated:
        print("   Added new entries to pub_topics.yaml")
    else:
        print("   No new entries to add")

    print("\n" + "=" * 60)
    print("Import complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review site/data/pub_topics.yaml and adjust topics as needed")
    print("2. Run: python scripts/bib2json.py site/data/publications.bib site/data/publications.json site/data/pub_topics.yaml")
    print("3. Build site: ./scripts/build.sh (or just hugo in site/)")
    print("")


if __name__ == '__main__':
    main()
