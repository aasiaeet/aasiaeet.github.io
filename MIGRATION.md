# Migration Guide: Jekyll to Hugo + Quartz

This document describes the migration from Jekyll (Minimal Mistakes) to Hugo (PaperModX) with Quartz notes.

## Current Status

- **Branch:** `migrate-hugo-quartz`
- **Status:** Ready for testing
- **Theme:** PaperModX (with floating ToC sidebar)
- **Deployment:** GitHub Pages via GitHub Actions
- **Original site:** Jekyll with Minimal Mistakes theme (still on `master` branch)

## New Directory Structure

```
repo/
├── .github/
│   └── workflows/
│       └── pages.yml         # GitHub Actions deployment
├── MIGRATION.md              # This file
├── netlify.toml              # Optional Netlify config (backup)
├── scripts/
│   ├── build.sh              # Full production build
│   ├── bib2json.py           # BibTeX to JSON converter
│   ├── dev.sh                # Hugo development server
│   └── dev-quartz.sh         # Quartz development server
├── site/                     # Hugo site
│   ├── hugo.yaml             # Hugo configuration
│   ├── assets/
│   │   └── css/extended/
│   │       └── custom.css    # Typography & styling overrides
│   ├── content/              # Content pages
│   │   ├── blog/             # Blog posts
│   │   ├── research/         # Research page
│   │   ├── publications/     # Publications page (by year)
│   │   ├── publicationbyyear/# Publications by year (alias)
│   │   ├── publicationbytopic/# Publications by topic
│   │   ├── teaching/         # Teaching page
│   │   ├── join/             # Join us page
│   │   └── bio/              # Extended bio
│   ├── data/                 # Data files
│   │   ├── publications.bib  # BibTeX source
│   │   ├── publications.json # Generated JSON
│   │   └── pub_topics.yaml   # Topic mapping
│   ├── layouts/              # Custom layouts
│   │   └── partials/
│   │       ├── math.html     # KaTeX math rendering
│   │       ├── comments.html # Giscus comments
│   │       └── extend_head.html
│   ├── static/               # Static files
│   │   ├── images/           # Images
│   │   ├── cv/               # CV PDF
│   │   └── notes/            # Quartz output (generated)
│   └── themes/
│       └── PaperModX/        # PaperModX theme (git submodule)
├── quartz/                   # Quartz notes garden
│   ├── quartz.config.ts      # Quartz configuration
│   ├── content/              # Notes (Obsidian-compatible)
│   └── public/               # Built output (copied to site/static/notes)
└── (existing Jekyll files - untouched)
```

## Local Development

### Prerequisites

- **Hugo:** v0.147.0+ (extended version)
- **Node.js:** v22+
- **npm:** v10.9.2+

### Install Hugo (if not installed)

```bash
# Download and install to ~/bin
curl -L https://github.com/gohugoio/hugo/releases/download/v0.147.0/hugo_extended_0.147.0_linux-amd64.tar.xz | tar xJ -C ~/bin hugo
export PATH=$PATH:~/bin
```

### Install Node 22 (if not installed)

```bash
curl -fsSL https://nodejs.org/dist/v22.12.0/node-v22.12.0-linux-x64.tar.xz | tar xJ -C ~/bin --strip-components=1
export PATH=$HOME/bin/bin:$PATH
```

### Run Development Server

```bash
# From repo root
./scripts/dev.sh

# Site available at http://localhost:1313
```

### Run Quartz Separately (for notes editing)

```bash
# In a separate terminal
./scripts/dev-quartz.sh

# Notes available at http://localhost:8080
```

### Build for Production

```bash
./scripts/build.sh

# Output in site/public/
```

## GitHub Pages Deployment (Primary)

### Setup (One-time)

1. Go to your repo on GitHub
2. Settings → Pages
3. Under "Build and deployment", select **GitHub Actions** as source
4. The workflow in `.github/workflows/pages.yml` handles the rest

### How It Works

When you push to `master` (or `migrate-hugo-quartz` during testing):
1. GitHub Actions checks out the code
2. Installs Node 22 and Hugo
3. Builds Quartz notes
4. Builds Hugo site
5. Deploys to GitHub Pages

### Testing Before Merge

1. Push changes to `migrate-hugo-quartz` branch
2. GitHub Actions will build (check Actions tab)
3. Create a PR to see the build status
4. After merge to master, site deploys automatically

### Custom Domain

Your custom domain (`www.amirasiaee.com`) is configured in:
- `site/hugo.yaml` → `baseURL`
- GitHub repo Settings → Pages → Custom domain

## Rollback Plan

### Quick Rollback

Since the old Jekyll code is still on `master`, you can rollback by:

1. Reverting the merge commit:
```bash
git revert <merge-commit-sha>
git push
```

2. Or reset to the commit before merge:
```bash
git log --oneline  # Find the commit before merge
git reset --hard <commit-hash>
git push --force
```

### Temporary Disable New Site

If GitHub Actions is failing:
1. Go to Settings → Pages
2. Change source to "Deploy from a branch"
3. Select `master` branch and `/` (root)
4. This will serve the old Jekyll _site if it exists

## Theme Features

### Floating Table of Contents

PaperModX provides a floating ToC sidebar on the right side for desktop screens.

**Global setting** (in `hugo.yaml`):
```yaml
params:
  TocSide: 'right'  # 'right', 'left', or remove for no floating ToC
  showtoc: true
  tocopen: true
```

**Per-page control** (in front matter):
```yaml
---
title: "My Post"
toc: true      # Show ToC (default: true for posts)
tocopen: true  # Start expanded
---
```

### Typography

Custom fonts are set in `site/assets/css/extended/custom.css`:

```css
:root {
  --font-body: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-heading: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, monospace;
}
```

To change fonts, edit the CSS variables in that file.

### Homepage Layout

The homepage uses `homeInfoParams` (not profile mode) for a cleaner, less author-centered look. Edit in `hugo.yaml`:

```yaml
params:
  homeInfoParams:
    Title: "Your Name"
    Content: |
      Your description here...
```

## Giscus Comments Setup

To enable Giscus comments on blog posts:

1. Go to your GitHub repo settings
2. Enable **Discussions** feature
3. Go to [giscus.app](https://giscus.app/)
4. Configure with your repo
5. Copy the `data-repo-id` and `data-category-id`
6. Update `site/hugo.yaml`:

```yaml
params:
  giscus:
    repo: "aasiaeet/aasiaeet.github.io"
    repoId: "<your-repo-id>"
    category: "Announcements"
    categoryId: "<your-category-id>"
```

## Content Migration Notes

### Blog Posts

Jekyll front matter:
```yaml
---
title: "Post Title"
categories:
  - Category
tag:
  - Tag
---
```

Hugo front matter:
```yaml
---
title: "Post Title"
date: 2018-01-22
categories:
  - Category
tags:
  - Tag
summary: "Brief description"
math: true  # Enable if post has math
toc: true   # Enable ToC sidebar
---
```

### Math Rendering

- Jekyll: `$$...$$` for display, inline varied
- Hugo: Same syntax, using KaTeX
- Quartz: Same syntax, using KaTeX

### Images

- Jekyll: `{{ site.url }}{{ site.baseurl }}/assets/images/file.jpg`
- Hugo: `/images/file.jpg`

### Remaining Migration Tasks

The following blog posts still need migration:
- `2018-01-10-r-indexing.md`
- `2018-01-11-r-merge.md`
- `2018-01-12-pandoc.md`
- `2018-01-13-KaTex for Jekyll.md`
- `2018-01-15-r-factor-indexing.md`
- `2018-01-17-cll-ibrutinib-resistence.md`
- `2018-01-18-jekyll-scholar.md`
- `2018-01-20-staticman-vs-disqus.md`
- `2018-01-25-miracle-fresh-eyes.md`
- `2018-01-26-trello.md`

## Publications Management

Publications are managed via BibTeX as the canonical source, converted to JSON for Hugo templates.

### File Structure

```
site/data/
├── publications.bib     # Canonical BibTeX source
├── publications.json    # Generated (do not edit manually)
└── pub_topics.yaml      # Topic mapping for each publication
site/static/publications/
└── *.pdf                # PDF files (named by BibTeX key)
```

### Quick Update from Zotero

The easiest way to update publications is from Zotero:

```bash
# 1. In Zotero: Right-click collection → Export Collection
#    - Format: BibTeX
#    - Check "Export Files"
#    - Save to: site/mypapers/mypapers.bib

# 2. Run the update script
./scripts/update_publications.sh

# 3. Review topics (optional)
# Edit site/data/pub_topics.yaml if needed

# 4. Rebuild site
./scripts/build.sh
```

The script automatically:
- Extracts PDFs from Zotero's nested folder structure
- Renames them using BibTeX keys (e.g., `author_title_2024.pdf`)
- Generates clean BibTeX (removes Zotero-specific fields)
- Auto-suggests topics based on title/abstract keywords
- Converts to JSON for Hugo templates

See `scripts/README.md` for detailed documentation.

### Adding a New Publication Manually

1. **Add the BibTeX entry** to `site/bib/publications.bib`:

```bibtex
@article{abc24,
  title = "Your Paper Title",
  author = {Last, First and Another, Author},
  journal = "Journal Name",
  year = 2024,
  volume = 1,
  pages = "1--10",
  note = "https://doi.org/10.xxxx/xxxxxx"
}
```

2. **Add topic mapping** (optional) to `site/data/pub_topics.yaml`:

```yaml
abc24:
  - Machine Learning
  - Computational Biology
```

3. **Add PDF file** (optional): Copy the PDF to `site/static/publications/abc24.pdf` (use the BibTeX key as filename).

4. **Rebuild**: Run `./scripts/build.sh` or push to trigger GitHub Actions.

### How It Works

1. The `scripts/bib2json.py` script converts BibTeX to JSON
2. It reads topic mappings from `pub_topics.yaml`
3. Hugo templates read `publications.json` and render:
   - `/publications/` - Main publications page (by year)
   - `/publicationbyyear/` - Publications grouped by year
   - `/publicationbytopic/` - Publications grouped by topic

### BibTeX Fields

The converter extracts these fields:

| BibTeX Field | JSON Field | Notes |
|--------------|------------|-------|
| key | key | The citation key (e.g., `abc24`) |
| title | title | Paper title |
| author | authors | Parsed into array of names |
| year | year | Publication year |
| journal/booktitle | venue | Venue name |
| volume | volume | Optional |
| number | number | Optional |
| pages | pages | Optional |
| doi | doi | Optional |
| url | url | Optional (also extracted from `note`) |
| keywords | tags | Comma-separated keywords |

### Topic Categories

If no topic is specified in `pub_topics.yaml`, publications are auto-assigned:
- **Journal Articles** - for `@article` entries
- **Conference Papers** - for `@inproceedings`, `@conference` entries
- **Other** - for all other types

### PDF Linking

PDFs are automatically linked if they exist in `site/static/publications/` with the BibTeX key as filename. For example:
- BibTeX key: `gabz15`
- PDF path: `site/static/publications/gabz15.pdf`
- Link generated: `/publications/gabz15.pdf`

## Netlify (Optional/Backup)

The `netlify.toml` file is included as a backup option. If you prefer Netlify:

1. Connect repo to Netlify
2. Netlify will use `netlify.toml` configuration
3. Build command: `bash scripts/build.sh`
4. Publish directory: `site/public`

## Quality Checklist

Before switching to production, verify:

- [ ] Hugo site matches current site content
- [ ] Mobile layout looks clean
- [ ] Floating ToC works on desktop
- [ ] Typography feels neutral and academic
- [ ] Homepage is not profile-centered
- [ ] Fast load, minimal JS
- [ ] Math renders correctly in blog posts
- [ ] Giscus comments work (if configured)
- [ ] `/notes` loads correctly
- [ ] Wikilinks work in notes
- [ ] Backlinks work in notes
- [ ] No broken links
- [ ] 404 page exists
- [ ] GitHub Actions build is green

## Support

For issues with:
- **Hugo:** https://discourse.gohugo.io/
- **PaperModX:** https://github.com/reorx/hugo-PaperModX/issues
- **Quartz:** https://github.com/jackyzha0/quartz/discussions
