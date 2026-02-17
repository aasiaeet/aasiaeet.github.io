# Website Maintenance Notes

Internal reference for maintaining amirasiaee.com. Not published on the site.

## Architecture Overview

- **Framework:** Hugo (PaperModX theme) + Quartz (for notes/graph, currently disabled)
- **Hosting:** GitHub Pages via GitHub Actions (`.github/workflows/pages.yml`)
- **Domain:** amirasiaee.com (configured via CNAME)
- **Repo structure:**
  - `site/` - Hugo site (content, layouts, config, data, static assets)
  - `quartz/` - Quartz setup for interconnected notes with graph view (currently disabled)
  - `scripts/` - Build and publication management scripts

## Updating Publications

### Quick workflow (from Zotero / Google Scholar)

```bash
# 1. Export from Zotero:
#    Right-click collection -> Export Collection
#    Format: BibTeX, check "Export Files"
#    Save to: site/mypapers/mypapers.bib

# 2. Preview what will change (safe, no files modified)
python3 scripts/import_zotero.py --dry-run

# 3. Run the update pipeline
./scripts/update_publications.sh

# 4. Review auto-generated topics
#    Edit site/data/pub_topics.yaml if needed

# 5. Commit and push (GitHub Actions builds and deploys automatically)
```

### Merge protection (re-importing safely)

The import script matches new Zotero entries against existing `publications.bib`
using **DOI** (exact match) and **title** (fuzzy match, 85% similarity threshold).
When a match is found:

- **BibTeX key is preserved** -- existing key is kept, so topic mappings and PDFs
  remain linked.
- **Year drift is blocked for preprints** -- if an arXiv/bioRxiv paper's year
  changed (e.g., Google Scholar reports 2026 for a 2023 preprint), the original
  year is kept. Exception: if the entry type changed from `misc` to `article`
  (preprint got published), the new year is accepted.
- **New entries are added** without affecting existing ones.
- A **merge report** is printed showing all matches, key remappings, and year
  changes.

Use `--dry-run` to preview all of this before any files are modified.

### Adding Zenodo papers (not on Google Scholar)

Zenodo papers won't be in Google Scholar, so add them manually:

```bash
# 1. Add BibTeX entry to site/bib/publications.bib
#    Use @misc type with publisher = {Zenodo}
#    Include doi and url fields
# 2. Add topic mapping to site/data/pub_topics.yaml
# 3. Regenerate JSON:
python3 scripts/bib2json.py site/bib/publications.bib site/data/publications.json site/data/pub_topics.yaml
# 4. Commit and push
```

These manually added entries will be preserved when re-importing from Zotero
(matched by DOI or title).

### Manual workflow (without Zotero)

```bash
# 1. Add BibTeX entry to site/bib/publications.bib
# 2. Add topic mapping to site/data/pub_topics.yaml
# 3. Optionally copy PDF to site/static/publications/{bibtex_key}.pdf
# 4. Regenerate JSON:
python3 scripts/bib2json.py site/bib/publications.bib site/data/publications.json site/data/pub_topics.yaml
# 5. Commit and push
```

### Key files

| File | Purpose |
|------|---------|
| `site/bib/publications.bib` | Clean BibTeX source (what the site reads) |
| `site/data/publications.json` | Generated JSON used by Hugo templates |
| `site/data/pub_topics.yaml` | Manual topic assignments per paper (by BibTeX key) |
| `site/mypapers/mypapers.bib` | Raw Zotero export (input to import script) |
| `scripts/update_publications.sh` | Main update script (runs import + bib2json) |
| `scripts/import_zotero.py` | Imports from Zotero with merge protection |
| `scripts/bib2json.py` | Converts BibTeX to JSON, applies topic mappings |
| `site/layouts/_default/publications.html` | Hugo template for publications-by-year view |
| `site/layouts/_default/publications-by-topic.html` | Hugo template for publications-by-topic view |
| `site/layouts/partials/publication-item.html` | Single publication item partial |

### What depends on BibTeX keys (why stability matters)

Everything is keyed off the BibTeX citation key (e.g., `asiaee_high_2023`):
- `pub_topics.yaml` topic mappings
- `publications.json` entries
- PDF filenames in `site/static/publications/{key}.pdf`
- The publication numbering on the website

If keys change, topic mappings become orphaned and PDFs get disconnected.
The merge logic in `import_zotero.py` prevents this.

### Topic classification

Topics are auto-suggested by `import_zotero.py` based on keywords in title/abstract.
Override manually in `site/data/pub_topics.yaml`:

```yaml
paper_key_2024:
  - Primary Topic
  - Secondary Topic
```

The `_featured` key in `pub_topics.yaml` can list keys of papers to highlight.

## Currently Disabled Features

### Notes Section (Quartz graph)

**What it was:** An interconnected notes system using Quartz with a graph visualization.
Content lives in `quartz/content/` (Markdown files on topics like Bioinformatics, ML, Causal Inference, etc.).

**How to re-enable:**

1. Uncomment the Notes menu item in `site/hugo.yaml`:
   ```yaml
   - identifier: notes
     name: Notes
     url: /notes/
     weight: 60
   ```

2. Uncomment the Quartz build steps in `.github/workflows/pages.yml`:
   - "Setup Node.js" step
   - "Install Quartz dependencies" step
   - "Build Quartz" step
   - "Copy Quartz output to Hugo static" step

3. For local builds, also update `scripts/build.sh` if needed (it currently
   has the Quartz build steps).

4. Quartz content is in `quartz/content/`. Add/edit Markdown files there
   to create interconnected notes with `[[wiki-links]]`.

### Blog Section

**What it was:** A blog with posts (e.g., the K99 grant writing guide).
Content lives in `site/content/blog/`.

**How to re-enable:**

1. Uncomment the Blog menu item in `site/hugo.yaml`:
   ```yaml
   - identifier: blog
     name: Blog
     url: /blog/
     weight: 40
   ```

2. Existing content:
   - `site/content/blog/_index.md` - Blog listing page
   - `site/content/blog/2019-03-02-early-k99.md` - K99 grant writing guide

3. To add new posts, create Markdown files in `site/content/blog/` with
   front matter:
   ```yaml
   ---
   title: "Post Title"
   date: 2026-01-15
   categories:
     - Category
   tags:
     - tag1
   summary: "Brief description"
   ---
   ```

## Deployment

Pushing to `master` triggers GitHub Actions which:
1. Converts BibTeX to JSON
2. Builds Hugo site
3. Deploys to GitHub Pages

The workflow file is at `.github/workflows/pages.yml`.

For local development:
```bash
cd site && hugo server -D
```

## Hugo Config

Main config: `site/hugo.yaml`

Key settings:
- Navigation menu items under `menu.main`
- Homepage content under `params.homeInfoParams`
- Social links under `params.socialIcons`
- Theme: PaperModX (git submodule in `site/themes/PaperModX`)
