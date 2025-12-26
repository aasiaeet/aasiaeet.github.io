#!/usr/bin/env python3
"""
Convert BibTeX file to JSON for Hugo site.

Usage: python bib2json.py <input.bib> <output.json> [topics.yaml]
"""

import re
import json
import sys
import yaml
from pathlib import Path


def parse_bibtex(content):
    """Parse BibTeX file and return list of entries."""
    entries = []

    # Match BibTeX entries: @TYPE{key, ... }
    # Handle nested braces properly
    entry_pattern = r'@(\w+)\s*\{\s*([^,]+)\s*,'

    # Find all entry starts
    for match in re.finditer(entry_pattern, content):
        entry_type = match.group(1).lower()
        key = match.group(2).strip()

        # Find the matching closing brace
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
            entry_content = content[start:pos-1]
            entry = parse_entry(entry_type, key, entry_content)
            if entry:
                entries.append(entry)

    return entries


def parse_entry(entry_type, key, content):
    """Parse a single BibTeX entry."""
    entry = {
        'key': key,
        'type': entry_type,
    }

    # Parse fields
    fields = {}

    # Match field = value patterns
    # Handle both {value} and "value" and bare values
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
            # Find matching closing brace
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
            # Find closing quote
            pos = start + 1
            while pos < len(content) and content[pos] != '"':
                pos += 1
            value = content[start+1:pos]
        else:
            # Bare value (number or macro)
            pos = start
            while pos < len(content) and content[pos] not in ',}\n':
                pos += 1
            value = content[start:pos].strip()

        # Clean up the value
        value = clean_value(value)
        fields[field_name] = value

    # Map fields to output format
    entry['title'] = fields.get('title', '')
    entry['authors'] = parse_authors(fields.get('author', ''))
    entry['year'] = parse_year(fields.get('year', ''))
    entry['abstract'] = fields.get('abstract', '')

    # Venue/journal
    if 'journal' in fields:
        entry['venue'] = fields['journal']
        entry['venue_type'] = 'journal'
    elif 'booktitle' in fields:
        entry['venue'] = fields['booktitle']
        entry['venue_type'] = 'conference'
    elif 'publisher' in fields:
        entry['venue'] = fields.get('publisher', '')
        entry['venue_type'] = 'book'
    else:
        entry['venue'] = ''
        entry['venue_type'] = entry_type

    # Additional metadata
    if 'volume' in fields:
        entry['volume'] = fields['volume']
    if 'number' in fields:
        entry['number'] = fields['number']
    if 'pages' in fields:
        entry['pages'] = fields['pages']

    # URLs, DOI, arXiv, and code
    entry['doi'] = fields.get('doi', '')
    entry['url'] = fields.get('url', '')
    entry['pdf'] = fields.get('pdf', '')
    entry['arxiv'] = fields.get('arxiv', fields.get('eprint', ''))
    entry['code'] = fields.get('code', fields.get('github', ''))

    # Check note field for URLs
    note = fields.get('note', '')
    if note and not entry['url']:
        url_match = re.search(r'https?://[^\s]+', note)
        if url_match:
            entry['url'] = url_match.group(0)

    # Keywords/tags
    keywords = fields.get('keywords', '')
    if keywords:
        entry['tags'] = [k.strip() for k in keywords.split(',')]
    else:
        entry['tags'] = []

    return entry


def clean_value(value):
    """Clean up a BibTeX value."""
    # Remove line breaks and extra whitespace
    value = ' '.join(value.split())
    # Remove LaTeX commands we don't need
    value = re.sub(r'\\textit\{([^}]+)\}', r'\1', value)
    value = re.sub(r'\\textbf\{([^}]+)\}', r'\1', value)
    value = re.sub(r'\\emph\{([^}]+)\}', r'\1', value)
    value = re.sub(r'\\\w+\s*', '', value)  # Remove other LaTeX commands
    # Clean up braces used for capitalization preservation
    value = value.replace('{', '').replace('}', '')
    return value.strip()


def parse_authors(author_str):
    """Parse author string into list of author names."""
    if not author_str:
        return []

    # Split by " and "
    authors = re.split(r'\s+and\s+', author_str)

    result = []
    for author in authors:
        author = author.strip()
        # Remove asterisks (equal contribution markers)
        author = author.replace('*', '')
        # Handle "Last, First" format
        if ',' in author:
            parts = author.split(',', 1)
            last = parts[0].strip()
            first = parts[1].strip() if len(parts) > 1 else ''
            author = f"{first} {last}".strip()
        result.append(author)

    return result


def parse_year(year_str):
    """Parse year from string."""
    if not year_str:
        return 0
    # Extract 4-digit year
    match = re.search(r'(\d{4})', str(year_str))
    if match:
        return int(match.group(1))
    return 0


def load_topic_mapping(topics_file):
    """Load topic mapping from YAML file.

    Supports two formats:
    1. Simple: key: [topics] or key: topic
    2. Extended: key: { topics: [...], featured: true }

    Also supports a special '_featured' key with list of featured publication keys.
    """
    if not topics_file or not Path(topics_file).exists():
        return {}, set()

    with open(topics_file, 'r') as f:
        data = yaml.safe_load(f) or {}

    # Extract featured list if present (handle None case when all items are commented)
    featured_list = data.pop('_featured', None) or []
    featured = set(featured_list)

    # Process topic mappings
    topic_mapping = {}
    for key, value in data.items():
        if isinstance(value, dict):
            # Extended format: {topics: [...], featured: true}
            topic_mapping[key] = value.get('topics', ['Unassigned'])
            if value.get('featured'):
                featured.add(key)
        elif isinstance(value, list):
            topic_mapping[key] = value
        elif isinstance(value, str):
            topic_mapping[key] = [value]

    return topic_mapping, featured


def add_topics(entries, topic_mapping, featured_keys):
    """Add topics and featured flag to entries based on manual mapping only.

    Publications without explicit mapping get 'Unassigned' topic.
    No auto-inference based on venue type.
    """
    for entry in entries:
        key = entry['key']
        if key in topic_mapping:
            topics = topic_mapping[key]
            if isinstance(topics, str):
                topics = [topics]
            entry['topics'] = topics
        else:
            # No auto-inference - mark as unassigned
            entry['topics'] = ['Unassigned']

        # Mark featured publications
        entry['featured'] = key in featured_keys

    return entries


def main():
    if len(sys.argv) < 3:
        print("Usage: python bib2json.py <input.bib> <output.json> [topics.yaml]")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    topics_file = sys.argv[3] if len(sys.argv) > 3 else None

    # Read BibTeX file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Parse entries
    entries = parse_bibtex(content)

    # Load and apply topic mapping
    topic_mapping, featured_keys = load_topic_mapping(topics_file)
    entries = add_topics(entries, topic_mapping, featured_keys)

    # Sort by year (descending) then by key
    entries.sort(key=lambda x: (-x['year'], x['key']))

    # Write JSON output
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)

    print(f"Converted {len(entries)} entries to {output_file}")


if __name__ == '__main__':
    main()
