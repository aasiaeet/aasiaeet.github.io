# Scripts Documentation (Internal)

This folder contains build and maintenance scripts for the website.
This documentation is for internal use and not visible on the website.

## Publication Management

### Quick Update Workflow

When you add new papers to Zotero and want to update the website:

```bash
# 1. Export from Zotero
#    - In Zotero: Right-click your collection → Export Collection
#    - Format: BibTeX
#    - Check "Export Files" checkbox
#    - Save to: site/mypapers/mypapers.bib

# 2. Run the update script
./scripts/update_publications.sh

# 3. (Optional) Review topics in site/data/pub_topics.yaml

# 4. Rebuild site
./scripts/build.sh
```

### Scripts Overview

| Script | Purpose |
|--------|---------|
| `update_publications.sh` | Main entry point - runs import + conversion |
| `import_zotero.py` | Imports from Zotero export, extracts PDFs, suggests topics |
| `bib2json.py` | Converts BibTeX to JSON for Hugo templates |
| `build.sh` | Full site build (Quartz + Hugo) |
| `dev.sh` | Hugo dev server |
| `dev-quartz.sh` | Quartz dev server |

### How It Works

1. **Zotero Export** (`site/mypapers/`)
   - Contains `mypapers.bib` and `files/` folder
   - Files folder has nested structure: `files/{id}/{filename}.pdf`

2. **import_zotero.py**
   - Parses Zotero BibTeX format
   - Extracts PDFs from nested folders → `site/static/publications/{key}.pdf`
   - Generates clean `publications.bib` (removes Zotero-specific fields)
   - Auto-suggests topics based on title/abstract keywords
   - Updates `pub_topics.yaml` with new entries

3. **bib2json.py**
   - Converts BibTeX to JSON for Hugo
   - Applies topic mapping from `pub_topics.yaml`
   - Outputs to `publications.json`

4. **Hugo Templates**
   - Read from `publications.json`
   - Render publication lists by year and by topic

### Topic Classification

Topics are auto-suggested based on keywords in title and abstract.

**Keyword Categories:**
- Computational Biology: gene, expression, transcriptome, miRNA, etc.
- Cancer Research: cancer, tumor, oncogenetic, etc.
- Machine Learning: learning, optimization, estimation, etc.
- Causal Inference: causal, treatment effect, DAG, etc.
- Social Networks: social, network, influence, etc.
- Immunology: immune, vaccine, T cell, etc.
- And more...

**Manual Override:**
Edit `site/data/pub_topics.yaml` to manually set or adjust topics:

```yaml
paper_key_2024:
  - Primary Topic
  - Secondary Topic
```

### LLM-Assisted Topic Refinement

When updating publications, you can ask Claude to help refine topics:

```
I just updated my publications using the import_zotero.py script.
Please review the auto-generated topics in site/data/pub_topics.yaml
and suggest improvements based on the actual paper content.
```

Claude can:
1. Read the generated `pub_topics.yaml`
2. Fetch abstracts from the BibTeX or URLs if needed
3. Suggest more accurate topic assignments
4. Update the YAML file with refined topics

### Adding a New Publication Manually

If not using Zotero:

1. Add BibTeX entry to `site/bib/publications.bib`
2. Add topic mapping to `site/data/pub_topics.yaml`
3. Copy PDF to `site/static/publications/{key}.pdf`
4. Run `python scripts/bib2json.py site/bib/publications.bib site/data/publications.json site/data/pub_topics.yaml`

### Troubleshooting

**PDFs not being copied:**
- Check that Zotero export has "Export Files" checked
- Check file permissions on `site/mypapers/files/`
- Run with verbose output: `python scripts/import_zotero.py --suggest-topics`

**Topics not appearing:**
- Ensure `pub_topics.yaml` uses the exact BibTeX key
- BibTeX keys from Zotero are like `author_title_year` format

**Build fails:**
- Run `python scripts/bib2json.py` manually to see errors
- Check that `publications.json` was generated
