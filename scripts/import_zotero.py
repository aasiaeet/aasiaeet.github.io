#!/usr/bin/env python3
"""
Import publications from Zotero export.

This script:
1. Reads mypapers.bib from Zotero export
2. Matches new entries against existing publications.bib by DOI or title
3. Preserves existing BibTeX keys and topic mappings for matched entries
4. Extracts PDFs from nested folder structure
5. Copies PDFs to site/static/publications/ with proper names
6. Generates clean publications.bib (merging new + existing)
7. Auto-generates topic suggestions based on titles/abstracts

Usage: python import_zotero.py [--suggest-topics] [--dry-run]

The --suggest-topics flag prints topic suggestions that can be reviewed
and added to pub_topics.yaml

The --dry-run flag shows what would change without modifying any files
"""

import re
import os
import sys
import shutil
import yaml
from pathlib import Path
from difflib import SequenceMatcher

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


def normalize_doi(doi):
    """Normalize a DOI for comparison."""
    if not doi:
        return ''
    doi = doi.strip().lower()
    # Remove common prefixes
    doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi)
    doi = re.sub(r'^doi:\s*', '', doi)
    return doi


def normalize_title(title):
    """Normalize a title for fuzzy comparison."""
    if not title:
        return ''
    # Remove LaTeX formatting
    title = re.sub(r'\\[a-zA-Z]+\{([^}]*)\}', r'\1', title)
    title = re.sub(r'[{}\\]', '', title)
    # Lowercase, strip punctuation, collapse whitespace
    title = title.lower()
    title = re.sub(r'[^a-z0-9\s]', '', title)
    title = ' '.join(title.split())
    return title


def titles_match(title1, title2, threshold=0.85):
    """Check if two titles are similar enough to be the same paper."""
    t1 = normalize_title(title1)
    t2 = normalize_title(title2)
    if not t1 or not t2:
        return False
    return SequenceMatcher(None, t1, t2).ratio() >= threshold


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


def load_existing_bib():
    """Load existing publications.bib and build lookup indices."""
    if not OUTPUT_BIB.exists():
        return [], {}, {}

    entries = parse_zotero_bib(OUTPUT_BIB)

    # Build DOI index: normalized_doi -> entry
    doi_index = {}
    for entry in entries:
        doi = normalize_doi(entry.get('doi', ''))
        if doi:
            doi_index[doi] = entry

    # Build title index: normalized_title -> entry
    title_index = {}
    for entry in entries:
        ntitle = normalize_title(entry.get('title', ''))
        if ntitle:
            title_index[ntitle] = entry

    return entries, doi_index, title_index


def match_entry(new_entry, doi_index, title_index):
    """Try to match a new entry against existing ones.

    Returns (existing_entry, match_method) or (None, None).
    Match priority: DOI (exact) > title (fuzzy).
    """
    # Try DOI match first (most reliable)
    new_doi = normalize_doi(new_entry.get('doi', ''))
    if new_doi and new_doi in doi_index:
        return doi_index[new_doi], 'doi'

    # Try title match (fuzzy)
    new_title = new_entry.get('title', '')
    new_ntitle = normalize_title(new_title)
    if new_ntitle:
        # Exact normalized title match
        if new_ntitle in title_index:
            return title_index[new_ntitle], 'title_exact'
        # Fuzzy title match
        for existing_ntitle, existing_entry in title_index.items():
            if titles_match(new_title, existing_entry.get('title', '')):
                return existing_entry, 'title_fuzzy'

    return None, None


def merge_entries(new_entries, existing_entries, doi_index, title_index):
    """Merge new entries with existing ones, preserving keys.

    Returns:
        merged: list of entries with stable keys
        report: dict with merge statistics and details
    """
    report = {
        'matched': [],        # (new_key, existing_key, method, year_changed)
        'new': [],            # new_key entries with no match
        'year_changes': [],   # (key, old_year, new_year)
        'duplicates': [],     # potential duplicates within new entries
    }

    merged = {}  # key -> entry (use dict to deduplicate)
    new_key_to_existing_key = {}  # track key remappings

    # First, add all existing entries (they keep their keys)
    for entry in existing_entries:
        merged[entry['_key']] = entry

    # Then process new entries
    for new_entry in new_entries:
        new_key = new_entry['_key']

        existing, method = match_entry(new_entry, doi_index, title_index)

        if existing:
            existing_key = existing['_key']
            new_key_to_existing_key[new_key] = existing_key

            # Check for year changes
            old_year = existing.get('year', '')
            new_year = new_entry.get('year', '')
            year_changed = old_year != new_year and old_year and new_year

            report['matched'].append((new_key, existing_key, method, year_changed))

            if year_changed:
                report['year_changes'].append((existing_key, old_year, new_year))

            # Merge: start from existing, overlay new data, but preserve
            # important fields that may be missing from the new import
            # (e.g., Zotero/Google Scholar exports often drop DOIs, URLs)
            updated = dict(existing)  # start with existing data
            # Overlay non-empty fields from new entry
            preserve_fields = {'_key', '_raw'}  # never overwrite these from new
            important_fields = {'doi', 'url', 'arxiv', 'eprint', 'code',
                                'github', 'note'}  # keep existing if new is empty
            for field, value in new_entry.items():
                if field in preserve_fields:
                    continue
                if field in important_fields:
                    # Only overwrite if new value is non-empty
                    if value and value.strip():
                        updated[field] = value
                else:
                    updated[field] = value
            updated['_key'] = existing_key

            # Preserve existing year unless entry type changed
            # (e.g., misc/preprint -> article means it was published)
            old_type = existing.get('_type', '')
            new_type = new_entry.get('_type', '')
            preprint_to_published = (
                old_type in ('misc', 'unpublished') and
                new_type in ('article', 'inproceedings')
            )
            if year_changed and not preprint_to_published:
                updated['year'] = old_year  # keep original year

            merged[existing_key] = updated
        else:
            # Genuinely new entry
            report['new'].append(new_key)
            merged[new_key] = new_entry

    return list(merged.values()), report, new_key_to_existing_key


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


def update_topics_file(suggestions, key_remappings=None):
    """Update pub_topics.yaml with new entries and remap changed keys.

    Args:
        suggestions: dict of key -> [topics] for new entries
        key_remappings: dict of new_key -> existing_key for remapped entries
    """
    # Load existing topics
    existing = {}
    if TOPICS_FILE.exists():
        with open(TOPICS_FILE, 'r') as f:
            existing = yaml.safe_load(f) or {}

    # Remap any keys that changed (shouldn't happen with merge, but safety net)
    if key_remappings:
        for new_key, existing_key in key_remappings.items():
            if new_key in existing and existing_key not in existing:
                # Old key had topics under new_key name, move to existing_key
                existing[existing_key] = existing.pop(new_key)

    # Merge - don't overwrite existing manually set topics
    updated = False
    for key, topics in suggestions.items():
        if key not in existing:
            existing[key] = topics
            updated = True

    # Clean up orphaned keys (keys in topics file but not in any bib entry)
    # Don't remove automatically - just report them
    # (user may have manually added entries not in Zotero)

    if updated:
        with open(TOPICS_FILE, 'w') as f:
            yaml.dump(existing, f, default_flow_style=False, sort_keys=True, allow_unicode=True)

    return updated


def print_merge_report(report):
    """Print a summary of the merge operation."""
    print("\n" + "=" * 60)
    print("MERGE REPORT")
    print("=" * 60)

    if report['matched']:
        print(f"\n  Matched entries (key preserved): {len(report['matched'])}")
        for new_key, existing_key, method, year_changed in report['matched']:
            marker = " [YEAR CHANGED]" if year_changed else ""
            if new_key != existing_key:
                print(f"    {new_key} -> {existing_key} (by {method}){marker}")

    if report['year_changes']:
        print(f"\n  Year changes detected (original year kept for preprints):")
        for key, old_year, new_year in report['year_changes']:
            print(f"    {key}: {old_year} -> {new_year}")
        print("    NOTE: If a preprint was published in a journal, update the")
        print("    entry type to 'article' and re-run to accept the new year.")

    if report['new']:
        print(f"\n  New entries added: {len(report['new'])}")
        for key in report['new']:
            print(f"    + {key}")

    if not report['matched'] and not report['new']:
        print("\n  No changes detected.")

    print("")


def main():
    suggest_topics_flag = '--suggest-topics' in sys.argv
    dry_run = '--dry-run' in sys.argv

    print("=" * 60)
    print("Zotero Import Script (with merge protection)")
    print("=" * 60)

    if dry_run:
        print("  *** DRY RUN - no files will be modified ***")

    # Check if Zotero export exists
    if not ZOTERO_BIB.exists():
        print(f"ERROR: Zotero export not found at {ZOTERO_BIB}")
        print("Please export your Zotero collection to site/mypapers/")
        sys.exit(1)

    print(f"\n1. Reading Zotero BibTeX from {ZOTERO_BIB}...")
    new_entries = parse_zotero_bib(ZOTERO_BIB)
    print(f"   Found {len(new_entries)} entries in Zotero export")

    print(f"\n2. Loading existing publications from {OUTPUT_BIB}...")
    existing_entries, doi_index, title_index = load_existing_bib()
    print(f"   Found {len(existing_entries)} existing entries")

    print(f"\n3. Merging entries (matching by DOI, then title)...")
    merged_entries, report, key_remappings = merge_entries(
        new_entries, existing_entries, doi_index, title_index
    )
    print(f"   Result: {len(merged_entries)} total entries")

    print_merge_report(report)

    if dry_run:
        print("DRY RUN complete. No files were modified.")
        return

    print(f"4. Copying PDFs to {OUTPUT_PDF_DIR}...")
    copied, missing = copy_pdfs(merged_entries)
    print(f"   Copied {len(copied)} PDFs")
    if missing:
        print(f"   Missing/not found: {len(missing)}")
        for key, path in missing[:5]:
            print(f"     - {key}: {path[:50]}...")

    print(f"\n5. Generating clean BibTeX at {OUTPUT_BIB}...")
    clean_bib = generate_clean_bib(merged_entries)
    OUTPUT_BIB.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_BIB, 'w', encoding='utf-8') as f:
        f.write(clean_bib)
    print(f"   Written {len(merged_entries)} entries")

    print(f"\n6. Suggesting topics...")
    suggestions = suggest_topics(merged_entries)

    if suggest_topics_flag:
        print("\n   Topic suggestions (review and add to pub_topics.yaml):")
        print("   " + "-" * 50)
        for key, topics in sorted(suggestions.items()):
            print(f"   {key}:")
            for t in topics:
                print(f"     - {t}")

    print(f"\n7. Updating {TOPICS_FILE}...")
    updated = update_topics_file(suggestions, key_remappings)
    if updated:
        print("   Added new entries to pub_topics.yaml")
    else:
        print("   No new entries to add")

    print("\n" + "=" * 60)
    print("Import complete!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Review the merge report above for any year changes or key remappings")
    print("2. Review site/data/pub_topics.yaml and adjust topics as needed")
    print("3. Run: python scripts/bib2json.py site/bib/publications.bib site/data/publications.json site/data/pub_topics.yaml")
    print("4. Build site: ./scripts/build.sh (or just hugo in site/)")
    print("")


if __name__ == '__main__':
    main()
