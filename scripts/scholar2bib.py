#!/usr/bin/env python3
"""
scholar2bib.py — Replaces the Zotero step entirely.

Fetches papers from Google Scholar, finds the latest arXiv/bioRxiv version
of each paper, downloads PDFs, and writes site/mypapers/mypapers.bib +
site/mypapers/files/ in the exact format expected by update_publications.sh.

After running this, the rest of the pipeline is unchanged:
    ./scripts/update_publications.sh

PDF strategy:
  - arXiv papers    → always downloads latest version from arXiv
  - bioRxiv/medRxiv → always downloads latest version via DOI URL
  - No PDF found    → reuses existing PDF if one is already on disk
                      (safe for papers > 2 years old that haven't changed)
  - Zenodo papers   → flagged for manual review every time

At the end, a REVIEW NEEDED section lists every paper that needs your attention.

Usage:
    python scripts/scholar2bib.py                  # uses saved author ID
    python scripts/scholar2bib.py --author-id ID   # set author ID (saves it)
    python scripts/scholar2bib.py --years 2        # only papers from last 2 years
    python scripts/scholar2bib.py --dry-run        # no downloads, just show plan

Install deps:
    pip install scholarly requests

Finding your Google Scholar author ID:
    Go to your Scholar profile → the URL contains:
    https://scholar.google.com/citations?user=XXXXXXXXX
    The XXXXXXXXX part is your author ID.
"""

import argparse
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from datetime import date, datetime
from difflib import SequenceMatcher
from pathlib import Path

import requests

# ── Paths ──────────────────────────────────────────────────────────────────────
SCRIPT_DIR   = Path(__file__).parent.resolve()
ROOT_DIR     = SCRIPT_DIR.parent
OUTPUT_DIR   = ROOT_DIR / "site" / "mypapers"
OUTPUT_BIB   = OUTPUT_DIR / "mypapers.bib"
OUTPUT_FILES = OUTPUT_DIR / "files"
CONFIG_FILE  = SCRIPT_DIR / "scholar_config.json"
CACHE_FILE   = SCRIPT_DIR / "scholar_cache.json"
EXISTING_BIB = ROOT_DIR / "site" / "bib" / "publications.bib"
EXISTING_PDF = ROOT_DIR / "site" / "static" / "publications"

CACHE_MAX_DAYS = 30   # reuse Scholar results for up to 30 days

# ── External APIs ──────────────────────────────────────────────────────────────
ARXIV_API    = "http://export.arxiv.org/api/query"
CROSSREF_API = "https://api.crossref.org/works"
S2_API       = "https://api.semanticscholar.org/graph/v1"

# ── Stop words for BibTeX key generation ──────────────────────────────────────
STOP = {'a','an','the','of','for','in','on','with','and','or','by','to','from',
        'via','under','based','using','towards','data','new','improved','approach'}


# ══════════════════════════════════════════════════════════════════════════════
# Existing publications index (to find old PDFs)
# ══════════════════════════════════════════════════════════════════════════════

def load_existing_index():
    """
    Returns a list of (key, title, year) from the existing publications.bib,
    used to find old PDF files on disk when no new PDF is available.
    """
    if not EXISTING_BIB.exists():
        return []

    text  = EXISTING_BIB.read_text(encoding='utf-8')
    index = []

    for m in re.finditer(r'@\w+\{(\S+),', text):
        key   = m.group(1).rstrip(',')
        block = text[m.start():m.start() + 2000]   # enough for one entry
        tm    = re.search(r'title\s*=\s*\{(.+?)\}', block, re.S)
        ym    = re.search(r'year\s*=\s*\{(\d{4})\}', block)
        if tm:
            title = re.sub(r'[{}\\]', '', tm.group(1)).strip()
            year  = ym.group(1) if ym else ''
            index.append((key, title, year))

    return index


def find_existing_pdf(title, existing_index):
    """
    Fuzzy-match title against existing index.
    Returns (key, pdf_path, year) if a matching PDF file exists on disk,
    else (None, None, None).
    """
    best_ratio = 0
    best       = (None, None, None)

    for key, etitle, eyear in existing_index:
        r = SequenceMatcher(None, normalize(title), normalize(etitle)).ratio()
        if r > best_ratio:
            best_ratio = r
            best       = (key, eyear)

    if best_ratio >= 0.80:
        key, eyear = best
        pdf = EXISTING_PDF / f"{key}.pdf"
        if pdf.exists():
            return key, pdf, eyear

    return None, None, None


# ══════════════════════════════════════════════════════════════════════════════
# Utilities
# ══════════════════════════════════════════════════════════════════════════════

def normalize(text):
    return ' '.join(re.sub(r'[^\w\s]', ' ', text.lower()).split())


def similar(a, b):
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()


def make_key(authors, title, year):
    first = (authors[0] if authors else 'unknown').strip()
    last  = first.split(',')[0] if ',' in first else first.split()[-1]
    last  = re.sub(r'[^a-z]', '', last.lower())
    words = re.sub(r'[^a-z0-9\s]', '', title.lower()).split()
    word  = next((w for w in words if w not in STOP and len(w) > 3),
                 words[0] if words else 'paper')
    return f"{last}_{word}_{year}"


def bib_authors(authors):
    return ' and '.join(authors)


def is_zenodo(url_hint):
    return 'zenodo.org' in (url_hint or '').lower()


# ══════════════════════════════════════════════════════════════════════════════
# Source finders
# ══════════════════════════════════════════════════════════════════════════════

def find_arxiv(title, hint_url=''):
    """Returns (arxiv_id, metadata_dict) or (None, None)."""
    m = re.search(r'arxiv\.org/(?:abs|pdf)/([0-9]{4}\.[0-9]+)', hint_url, re.I)
    if m:
        arxiv_id = m.group(1)
        return arxiv_id, _fetch_arxiv_meta(arxiv_id)

    clean = re.sub(r'[^\w\s]', ' ', title).strip()
    try:
        r = requests.get(ARXIV_API,
                         params={'search_query': f'ti:"{clean}"',
                                 'max_results': 5, 'sortBy': 'relevance'},
                         timeout=15)
        r.raise_for_status()
    except requests.RequestException:
        return None, None

    ns = {'a': 'http://www.w3.org/2005/Atom',
          'x': 'http://arxiv.org/schemas/atom'}
    try:
        root = ET.fromstring(r.text)
    except ET.ParseError:
        return None, None

    for entry in root.findall('a:entry', ns):
        entry_title = entry.findtext('a:title', '', ns).strip()
        if similar(title, entry_title) < 0.80:
            continue
        id_url = entry.findtext('a:id', '', ns)
        m2 = re.search(r'abs/([^v\s]+)', id_url)
        if not m2:
            continue
        arxiv_id = m2.group(1)
        authors  = [a.findtext('a:name', '', ns)
                    for a in entry.findall('a:author', ns)]
        cat = entry.find('x:primary_category', ns)
        return arxiv_id, {
            'title':         entry_title,
            'authors':       authors,
            'year':          entry.findtext('a:published', '', ns)[:4],
            'abstract':      entry.findtext('a:summary', '', ns).strip(),
            'primary_class': cat.get('term', '') if cat is not None else '',
            'doi':           entry.findtext('x:doi', '', ns),
            'journal_ref':   entry.findtext('x:journal_ref', '', ns),
        }
    return None, None


def _fetch_arxiv_meta(arxiv_id):
    try:
        r = requests.get(ARXIV_API,
                         params={'id_list': arxiv_id, 'max_results': 1},
                         timeout=15)
        r.raise_for_status()
    except requests.RequestException:
        return {}
    ns = {'a': 'http://www.w3.org/2005/Atom',
          'x': 'http://arxiv.org/schemas/atom'}
    try:
        root = ET.fromstring(r.text)
    except ET.ParseError:
        return {}
    entry = root.find('a:entry', ns)
    if entry is None:
        return {}
    authors = [a.findtext('a:name', '', ns)
               for a in entry.findall('a:author', ns)]
    cat = entry.find('x:primary_category', ns)
    return {
        'title':         entry.findtext('a:title', '', ns).strip(),
        'authors':       authors,
        'year':          entry.findtext('a:published', '', ns)[:4],
        'abstract':      entry.findtext('a:summary', '', ns).strip(),
        'primary_class': cat.get('term', '') if cat is not None else '',
        'doi':           entry.findtext('x:doi', '', ns),
        'journal_ref':   entry.findtext('x:journal_ref', '', ns),
    }


def find_biorxiv(title):
    """Returns (doi, metadata_dict) or (None, None) for bioRxiv/medRxiv."""
    # bioRxiv switched to 10.64898 prefix in 2026; CrossRef covers both
    try:
        r = requests.get(CROSSREF_API,
                         params={'query.bibliographic': title,
                                 'filter': 'type:posted-content',
                                 'rows': 5,
                                 'select': 'DOI,title,author,posted,abstract'},
                         headers={'User-Agent': 'scholar2bib/1.0 (research)'},
                         timeout=15)
        r.raise_for_status()
        items = r.json().get('message', {}).get('items', [])
    except (requests.RequestException, ValueError):
        return None, None

    for item in items:
        item_title = (item.get('title') or [''])[0]
        if similar(title, item_title) < 0.80:
            continue
        doi = item.get('DOI', '')
        # Accept both old (10.1101) and new (10.64898) bioRxiv prefixes,
        # and medRxiv (10.1101 with medrxiv in URL)
        if not any(x in doi for x in ['biorxiv', 'medrxiv', '10.1101', '10.64898']):
            # CrossRef doesn't embed server name in DOI; check title server via URL
            pass   # still accept — we check server below
        authors  = [f"{a.get('given','')} {a.get('family','')}".strip()
                    for a in item.get('author', []) if a.get('family')]
        posted   = (item.get('posted', {}).get('date-parts') or [['']])[0]
        abstract = re.sub(r'<[^>]+>', '', item.get('abstract', '')).strip()
        return doi, {
            'title':    item_title,
            'authors':  authors,
            'year':     str(posted[0]) if posted else '',
            'abstract': abstract,
            'doi':      doi,
        }
    return None, None


def find_s2_pdf(title):
    """Semantic Scholar open-access PDF as last resort. Returns URL or None."""
    try:
        r = requests.get(f"{S2_API}/paper/search",
                         params={'query': title,
                                 'fields': 'title,openAccessPdf',
                                 'limit': 3},
                         timeout=15)
        r.raise_for_status()
        papers = r.json().get('data', [])
    except (requests.RequestException, ValueError):
        return None
    for p in papers:
        if similar(title, p.get('title', '')) < 0.80:
            continue
        pdf = p.get('openAccessPdf')
        if pdf and pdf.get('url'):
            return pdf['url']
    return None


# ══════════════════════════════════════════════════════════════════════════════
# PDF downloader
# ══════════════════════════════════════════════════════════════════════════════

def download_pdf(url, dest):
    """Download PDF to dest. Returns True on success."""
    try:
        r = requests.get(url,
                         headers={'User-Agent': 'Mozilla/5.0 (research tool)'},
                         timeout=30, stream=True)
        r.raise_for_status()
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, 'wb') as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        if dest.stat().st_size < 2000:
            dest.unlink(); return False
        with open(dest, 'rb') as f:
            if not f.read(4).startswith(b'%PDF'):
                dest.unlink(); return False
        return True
    except Exception as e:
        print(f"      PDF failed: {e}")
        if dest.exists(): dest.unlink()
        return False


# ══════════════════════════════════════════════════════════════════════════════
# BibTeX builder
# ══════════════════════════════════════════════════════════════════════════════

FIELD_ORDER = ['author', 'title', 'year', 'journal', 'booktitle',
               'volume', 'number', 'pages', 'doi', 'eprint',
               'archivePrefix', 'primaryClass', 'url', 'abstract', 'note', 'file']


def build_entry(key, entry_type, fields, pdf_path=None):
    lines = [f'@{entry_type}{{{key},']
    seen  = set()
    for f in FIELD_ORDER:
        if f in fields and fields[f]:
            lines.append(f'  {f} = {{{fields[f]}}},')
            seen.add(f)
    for f, v in fields.items():
        if f not in seen and v:
            lines.append(f'  {f} = {{{v}}},')
    if pdf_path:
        rel = pdf_path.relative_to(OUTPUT_DIR)   # files/N/key.pdf
        lines.append(f'  file = {{:{rel}:application/pdf}},')
    lines.append('}')
    return '\n'.join(lines)


# ══════════════════════════════════════════════════════════════════════════════
# Per-paper processor
# ══════════════════════════════════════════════════════════════════════════════

def process(paper, idx, dry_run, existing_index):
    """
    Returns (key, bib_string, flag_dict) where flag_dict is non-None
    if this paper needs manual review.
    """
    bib     = paper.get('bib', {})
    title   = bib.get('title', '').strip()
    year    = str(bib.get('pub_year', '') or '')
    venue   = bib.get('venue', '') or bib.get('journal', '') or ''

    raw_authors = bib.get('author', '')
    authors = ([a.strip() for a in raw_authors.split(' and ') if a.strip()]
               if isinstance(raw_authors, str) else list(raw_authors or []))

    if not title:
        return None

    print(f"\n  [{idx}] {title[:65]}...")

    hint      = (paper.get('eprint_url') or '') + (paper.get('pub_url') or '')
    zenodo    = is_zenodo(hint)
    pdf_url   = None
    pdf_path  = None
    etype     = 'misc'
    fields    = {}

    # ── 1. Try arXiv ──────────────────────────────────────────────────────────
    time.sleep(1)
    arxiv_id, arxiv_meta = find_arxiv(title, hint)

    if arxiv_id:
        m  = arxiv_meta or {}
        a  = m.get('authors') or authors
        y  = m.get('year')    or year
        t  = m.get('title')   or title
        key = make_key(a, t, y)
        is_published = bool(m.get('doi') or m.get('journal_ref'))
        etype = 'article' if is_published else 'misc'
        fields = {
            'author':        bib_authors(a),
            'title':         t,
            'year':          y,
            'eprint':        arxiv_id,
            'archivePrefix': 'arXiv',
            'primaryClass':  m.get('primary_class', ''),
            'abstract':      m.get('abstract', ''),
            'url':           f'https://arxiv.org/abs/{arxiv_id}',
        }
        if m.get('doi'):        fields['doi']  = m['doi']
        if m.get('journal_ref'): fields['note'] = m['journal_ref']
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id}"
        print(f"      arXiv: {arxiv_id}")

    # ── 2. Try bioRxiv/medRxiv ────────────────────────────────────────────────
    elif not zenodo:
        time.sleep(1)
        bio_doi, bio_meta = find_biorxiv(title)
        if bio_doi:
            m      = bio_meta or {}
            a      = m.get('authors') or authors
            y      = m.get('year')    or year
            t      = m.get('title')   or title
            key    = make_key(a, t, y)
            server = 'medRxiv' if 'medrxiv' in bio_doi else 'bioRxiv'
            fields = {
                'author':   bib_authors(a),
                'title':    t,
                'year':     y,
                'doi':      bio_doi,
                'abstract': m.get('abstract', ''),
                'url':      f'https://doi.org/{bio_doi}',
                'note':     f'{server} preprint',
            }
            base    = 'medrxiv' if 'medrxiv' in bio_doi else 'biorxiv'
            pdf_url = f"https://www.{base}.org/content/{bio_doi}.full.pdf"
            print(f"      {server}: {bio_doi}")

    # ── 3. Fallback: published paper ──────────────────────────────────────────
    if not arxiv_id and not pdf_url and not zenodo:
        key     = make_key(authors, title, year)
        venue_l = venue.lower()
        if any(w in venue_l for w in ['proceedings','conference','workshop','symposium']):
            etype  = 'inproceedings'
            fields = {'author': bib_authors(authors), 'title': title,
                      'year': year, 'booktitle': venue,
                      'url':  paper.get('pub_url', '')}
        else:
            etype  = 'article'
            fields = {'author': bib_authors(authors), 'title': title,
                      'year': year, 'journal': venue,
                      'url':  paper.get('pub_url', '')}
        time.sleep(0.5)
        pdf_url = find_s2_pdf(title)
        if pdf_url:
            print(f"      Semantic Scholar PDF")

    # Zenodo: minimal entry, flag for review
    if zenodo:
        key    = make_key(authors, title, year)
        etype  = 'misc'
        fields = {'author': bib_authors(authors), 'title': title,
                  'year': year, 'url': paper.get('pub_url', '')}
        print(f"      Zenodo — flagged for manual review")

    # ── Download PDF ──────────────────────────────────────────────────────────
    if not dry_run and pdf_url:
        dest = OUTPUT_FILES / str(idx) / f"{key}.pdf"
        time.sleep(1)
        if download_pdf(pdf_url, dest):
            pdf_path = dest
            print(f"      PDF saved ({dest.stat().st_size // 1024} KB)")
        else:
            pdf_url = None   # download failed, fall through to existing check

    # ── If no new PDF: look for existing one on disk ──────────────────────────
    flag = None
    if not pdf_path:
        ex_key, ex_pdf, ex_year = find_existing_pdf(title, existing_index)
        paper_year = int(year) if year.isdigit() else 0
        age_years  = datetime.now().year - paper_year

        if zenodo:
            # Always flag Zenodo regardless of PDF status
            flag = {
                'type':    'ZENODO',
                'title':   title,
                'year':    year,
                'ex_key':  ex_key,
                'ex_pdf':  str(ex_pdf) if ex_pdf else None,
            }
            print(f"      → FLAGGED (Zenodo)")
        elif ex_pdf:
            if age_years >= 2:
                # Old paper + existing PDF → safe to reuse silently
                print(f"      → Reusing existing PDF: {ex_key}.pdf (paper is {age_years}y old)")
            else:
                # Recent paper, no new PDF but have old one — flag for review
                flag = {
                    'type':   'NO_NEW_PDF',
                    'title':  title,
                    'year':   year,
                    'ex_key': ex_key,
                    'ex_pdf': str(ex_pdf),
                    'note':   f'Old PDF on disk: {ex_key}.pdf — check if updated',
                }
                print(f"      → FLAGGED (recent, no new PDF, old exists: {ex_key}.pdf)")
        else:
            # No PDF anywhere
            flag = {
                'type':  'MISSING_PDF',
                'title': title,
                'year':  year,
                'note':  'No PDF found anywhere — manual action needed',
            }
            print(f"      → FLAGGED (no PDF anywhere)")

    return key, build_entry(key, etype, fields, pdf_path), flag


# ══════════════════════════════════════════════════════════════════════════════
# Main
# ══════════════════════════════════════════════════════════════════════════════

def load_config():
    return json.loads(CONFIG_FILE.read_text()) if CONFIG_FILE.exists() else {}


def save_config(cfg):
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2))


# ── Scholar result cache ───────────────────────────────────────────────────────

def load_cache(author_id):
    """Load cached Scholar results if they exist and are fresh enough."""
    if not CACHE_FILE.exists():
        return None
    try:
        c = json.loads(CACHE_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return None
    if c.get('author_id') != author_id:
        return None
    cache_date = datetime.strptime(c.get('date', '1970-01-01'), '%Y-%m-%d')
    age_days   = (datetime.now() - cache_date).days
    if age_days > CACHE_MAX_DAYS:
        print(f"   Cache is {age_days} days old (limit {CACHE_MAX_DAYS}) — will re-query Scholar")
        return None
    print(f"   Using cached Scholar results from {c['date']} ({age_days}d ago)")
    return c.get('papers', [])


def save_cache(author_id, papers):
    """Save Scholar results to cache."""
    # Strip non-serialisable objects scholarly may attach
    safe = []
    for p in papers:
        safe.append({
            'bib':        p.get('bib', {}),
            'eprint_url': p.get('eprint_url', ''),
            'pub_url':    p.get('pub_url', ''),
        })
    CACHE_FILE.write_text(json.dumps({
        'author_id': author_id,
        'date':      date.today().isoformat(),
        'papers':    safe,
    }, indent=2, default=str))
    print(f"   Scholar results cached → {CACHE_FILE.name}")


def print_review_section(flags):
    """Print a clear summary of papers needing manual attention."""
    if not flags:
        print("\n✓ No manual review needed.")
        return

    zenodo_flags  = [f for f in flags if f['type'] == 'ZENODO']
    no_new_flags  = [f for f in flags if f['type'] == 'NO_NEW_PDF']
    missing_flags = [f for f in flags if f['type'] == 'MISSING_PDF']

    print("\n" + "=" * 64)
    print("REVIEW NEEDED")
    print("=" * 64)

    if zenodo_flags:
        print(f"\n  ZENODO ({len(zenodo_flags)}) — verify PDF is current:")
        for f in zenodo_flags:
            ex = f"  old PDF on disk: {f['ex_key']}.pdf" if f['ex_key'] else "  no PDF on disk"
            print(f"    • {f['title'][:60]} ({f['year']})")
            print(f"      {ex}")

    if no_new_flags:
        print(f"\n  RECENT, NO NEW PDF ({len(no_new_flags)}) — check if PDF changed:")
        for f in no_new_flags:
            print(f"    • {f['title'][:60]} ({f['year']})")
            print(f"      {f['note']}")

    if missing_flags:
        print(f"\n  MISSING PDF ({len(missing_flags)}) — provide PDF manually:")
        for f in missing_flags:
            print(f"    • {f['title'][:60]} ({f['year']})")

    print()


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--author-id', help='Google Scholar author ID (saved after first use)')
    parser.add_argument('--years', type=int, default=None,
                        help='Only papers from the last N years')
    parser.add_argument('--dry-run', action='store_true',
                        help='Print plan without downloading')
    parser.add_argument('--refresh', action='store_true',
                        help='Force a new Scholar query even if cache is fresh')
    args = parser.parse_args()

    cfg = load_config()
    if args.author_id:
        cfg['author_id'] = args.author_id
        save_config(cfg)
    author_id = cfg.get('author_id')
    if not author_id:
        print("ERROR: Run with --author-id YOUR_SCHOLAR_ID once to save it.")
        sys.exit(1)

    print("=" * 64)
    print("scholar2bib")
    print("=" * 64)
    print(f"\nAuthor ID : {author_id}")
    if args.years:
        print(f"Year filter: last {args.years} years (>= {datetime.now().year - args.years + 1})")
    if args.dry_run:
        print("DRY RUN: no files will be written")
    if args.refresh:
        print("--refresh: will re-query Scholar and overwrite cache")

    # ── Load existing publications for PDF reuse check ────────────────────────
    existing_index = load_existing_index()
    print(f"\nLoaded {len(existing_index)} existing entries for PDF reuse check")

    # ── Fetch Scholar profile (or load from cache) ────────────────────────────
    print(f"\n1. Fetching Scholar paper list...")
    papers = None if args.refresh else load_cache(author_id)

    if papers is None:
        # Need to query Scholar
        print("   Querying Google Scholar (this can be slow)...")
        try:
            from scholarly import scholarly
        except ImportError:
            print("ERROR: Run:  pip install scholarly requests")
            sys.exit(1)
        try:
            author = scholarly.search_author_id(author_id)
            author = scholarly.fill(author, sections=['publications'])
        except Exception as e:
            print(f"\nERROR: {e}")
            print("\nTips if Scholar blocked you:")
            print("  • Wait 10–15 min and retry")
            print("  • Use a VPN or mobile hotspot")
            print("  • Set env var SCRAPER_API_KEY if you have a ScraperAPI account")
            sys.exit(1)

        raw_papers = author.get('publications', [])
        print(f"   {len(raw_papers)} papers found — filling details (slow)...")

        # Fill each paper and accumulate into cache as we go
        papers = []
        for i, p in enumerate(raw_papers):
            try:
                time.sleep(2)
                p = scholarly.fill(p)
            except Exception as e:
                print(f"   [{i}] fill failed: {e} — storing partial")
            papers.append(p)
            if (i + 1) % 5 == 0:
                print(f"   [{i+1}/{len(raw_papers)}] filled so far — pausing 8s...")
                time.sleep(8)

        save_cache(author_id, papers)
    else:
        print(f"   {len(papers)} papers loaded from cache (no Scholar query needed)")

    if args.years:
        cutoff = datetime.now().year - args.years + 1
        papers = [p for p in papers
                  if int((p.get('bib') or {}).get('pub_year') or 0) >= cutoff]
        print(f"   {len(papers)} after year filter (>= {cutoff})")

    if not papers:
        print("Nothing to process.")
        sys.exit(0)

    # ── Process each paper ────────────────────────────────────────────────────
    print(f"\n2. Processing {len(papers)} papers...")

    entries    = []
    flags      = []
    keys_seen  = set()

    for i, paper in enumerate(papers):

        result = process(paper, i, args.dry_run, existing_index)
        if result:
            key, entry, flag = result

            # Deduplicate keys
            base, suffix = key, 2
            while key in keys_seen:
                key = f"{base}_{suffix}"; suffix += 1
            keys_seen.add(key)
            if key != base:
                entry = entry.replace(f'{{{base},', f'{{{key},', 1)

            entries.append((key, entry))
            if flag:
                flag['key'] = key
                flags.append(flag)

        if (i + 1) % 5 == 0 and i + 1 < len(papers):
            print(f"\n  --- {i+1}/{len(papers)} done, pausing 8s ---")
            time.sleep(8)

    # ── Write output ──────────────────────────────────────────────────────────
    print(f"\n3. {len(entries)} entries processed")

    if not args.dry_run:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(OUTPUT_BIB, 'w', encoding='utf-8') as f:
            f.write(f"% Generated by scholar2bib.py  {date.today()}\n")
            f.write(f"% Scholar author: {author_id}\n\n")
            for _, entry in entries:
                f.write(entry); f.write('\n\n')
        print(f"   Written → {OUTPUT_BIB}")
        print(f"\nNext step:  ./scripts/update_publications.sh")
    else:
        print("\nDRY RUN — would write:")
        for key, _ in entries:
            print(f"  {key}")

    # ── Always print review section ───────────────────────────────────────────
    print_review_section(flags)


if __name__ == '__main__':
    main()
