# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

Static website for Dulzumat, an artisan pastry shop in Valencia, Spain. Built with [Hugo](https://gohugo.io/) using a customized `hargo` theme, managed via Netlify CMS, deployed to two environments:
- **Staging**: Netlify auto-deploys on every push → `https://dulzumat.ge.org.es`
- **Production**: GitHub Actions CI (manual trigger) → FTP upload to `https://www.dulzumat.com`

## Development Commands

```bash
# Start local dev server (live reload at http://localhost:1313)
hugo server

# Build the site (output goes to public/)
hugo --gc --minify
```

Hugo version: **0.152.2** (see `netlify.toml` and `.github/workflows/main.yml`).

## Architecture

### Content & Data

- `content/` — Hugo Markdown pages. Product pages live under `content/productos/{category}/` (pasteles, tartas, reposteria, bolleria, salado, pan).
- `data/` — YAML data files used by templates:
  - `homepage.yml` — controls all homepage sections (banner, promo, video, cta, productos)
  - `orders.yml` — encargos page content
  - `contact.yml` — store locations/hours
  - `productos.yml` — allergen definitions (14 EU allergens, referenced by number in product front matter)
- `static/` — Static assets. Product images go in `static/images/products/`. Gallery images go in `static/images/galeria/` (adding/removing files there updates the gallery automatically).

### Theme (`themes/hargo/`)

Custom theme (not an upstream dependency—edit freely). Key locations:
- `layouts/` — Hugo templates for each section. Section-specific layouts override the generic ones (e.g., `layouts/productos/single.html` for product detail pages).
- `assets/scss/` — SCSS stylesheets. `_dulzumat.scss` contains Dulzumat-specific overrides. `_variables.scss` for colors/fonts.
- `archetypes/productos.md` — Template for new product pages.

### Product Pages

Product front matter fields (defined in `static/admin/config.yml` and the archetype):
```yaml
title: Product Name
price: "2,60 €"
clarification: "(optional note)"  # optional
weight: 1000                       # controls sort order (lower = first)
images:
  - images/products/filename.jpg   # gallery images
preview: images/products/filename-thumb.jpg
allergens: "1,3,7"                 # comma-separated allergen IDs from data/productos.yml
type: productos
```

### CMS

Netlify CMS at `/admin` (configured in `static/admin/config.yml`). Manages:
- Homepage sections via `data/homepage.yml`
- Encargos via `data/orders.yml`
- Contact info via `data/contact.yml`
- Products in each category folder under `content/productos/`

## Deployment

**Staging** (automatic): Any push to `master` triggers Netlify to rebuild and deploy.

**Production** (manual): Go to GitHub Actions → CI workflow → "Run workflow" on `master`. This builds with Hugo and FTP-syncs `public/` to the hosting server. FTP credentials are stored as GitHub secrets (`FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`).
