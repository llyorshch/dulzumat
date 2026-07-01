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

### Template Routing

- `themes/hargo/layouts/baseof.html` is the site shell. It includes the shared head, header, footer, and a `main` block filled by each page template.
- `themes/hargo/layouts/index.html` renders the homepage from `data/homepage.yml`. Most homepage sections are toggled purely by `enable` booleans in that data file.
- `themes/hargo/layouts/productos/list.html` renders product category landing pages such as `/productos/pasteles/`. It loops over `.Data.Pages` and shows either `preview` or the first image.
- `themes/hargo/layouts/productos/single.html` renders individual product pages. It expects front matter fields like `images`, `price`, `clarification`, and `allergens`.
- `themes/hargo/layouts/contacto/list.html` renders the contact page from `data/contact.yml`.
- `themes/hargo/layouts/encargos/list.html` renders the custom orders page from `data/orders.yml`.
- `themes/hargo/layouts/galeria/list.html` renders the gallery page body; the actual gallery content comes from shortcodes in `content/galeria/_index.md`.

### Representative Content Model

- Section pages such as `content/productos/pasteles/_index.md` define the title, ordering, and category hero image for each product category.
- Individual products are almost entirely front matter driven. Many product files have no markdown body at all; if a body is added, `layouts/productos/single.html` shows it under the "Descripcion" tab.
- The top-level `content/productos/_index.md` provides the intro content for the products landing page, and child section pages become the category cards.
- The gallery page is maintained by adding/removing images under `static/images/galeria/`; editors do not need to change template code for gallery updates.

### Styling & Frontend Behavior

- Main SCSS entrypoint: `themes/hargo/assets/scss/style.scss`.
- Dulzumat-specific visual overrides live in `themes/hargo/assets/scss/_dulzumat.scss`; most of the remaining SCSS comes from the Hargo theme.
- Main JS entrypoint: `themes/hargo/assets/js/script.js`. It handles the preloader, sticky nav styling, video modal behavior, Slick sliders, and accordion icon toggling.
- PhotoSwipe gallery behavior is loaded from `static/js/load-photoswipe.js`, but only when the `load-photoswipe` shortcode is used on a page.

### Operational Notes / Gotchas

- This repo is content-heavy and logic-light. Most changes should be made in `content/`, `data/`, `static/images/`, or a small number of templates rather than by introducing new code.
- `config.toml` still contains legacy theme features that are currently disabled or unused, including Snipcart, rating widgets, and generic blog-style list/single templates.
- The homepage "Nuestras especialidades" section in `layouts/index.html` currently ranges over pages with `Type == "especialidad"`. There are no such pages in the repository now, so this section renders only its heading unless matching content is added or the template is changed.
- Footer contact details are duplicated: store addresses/phones exist both in `config.toml` and, in richer form, in `data/contact.yml`. The footer uses `config.toml`; the contact page uses `data/contact.yml`.
- `themes/hargo/layouts/_partials/head.html` and `_partials/footer.html` include several third-party assets directly from CDNs or external services, including Netlify Identity, Google Maps, Snipcart, and PhotoSwipe.
- `netlify.toml` builds the canonical staging deployment from Hugo. `wrangler.jsonc` is also configured to build/publish the generated `public/` directory, so deployment assumptions should be checked before changing hosting behavior.

## Product Thumbnails

All product thumbnails (`preview` field) must match these specs — verified against the full Pasteles category:

| Property | Value |
|---|---|
| Dimensions | 620 × 620 px |
| Aspect ratio | 1:1 (square) |
| Format | JPEG |
| File size | ~60–150 KB |
| Margin | ~20px white space around the subject |

### Consistency rule: thumbnail and main image must match

The white border around the subject must be **identical** in both the thumbnail (shown in the category listing) and the main image (shown in the product detail page). Use the **same canvas crop** for both — only the output resolution differs:

| File | Output size |
|---|---|
| `<name>-thumb.jpg` | 620 × 620 px |
| `<name>.jpg` (main) | 1200 × 1200 px |

Both are generated from the same square canvas (e.g. 1128 px) centered on the subject centroid, then resized to their respective output sizes.

### Generating a thumbnail from a camera photo

Use `scripts/make-thumbnail.py` (requires Pillow: `pip install Pillow`):

```bash
python3 scripts/make-thumbnail.py <source_photo> static/images/products/<name>-thumb.jpg
```

**Key learnings baked into the script:**

- **Background detection**: camera photos have a near-white background (~RGB 231,231,233), not pure white. The script samples the four corners to detect it automatically.
- **Use centroid, not bounding box center**: the bounding box center is skewed by shadows and asymmetric edges. The centroid of the subject mask gives the true visual center.
- **Fill out-of-bounds with background colour**: when the square crop extends beyond the original frame, fill with the detected background colour (not white) to avoid visible seams.
- **Consistent threshold**: `diff > 20` per channel reliably isolates the pastry body without picking up faint shadows (`diff > 15`) or missing soft edges (`diff > 25`).

### Matching zoom across thumbnails

The script derives canvas size from the subject's bounding box width (`sw`). This works well for products with contained toppings, but **fails when decorations extend far from the body** (e.g. chocolate drizzle drips reaching the frame edges). In those cases `sw` is inflated and the subject appears too small.

**Rule**: when a new thumbnail looks under-zoomed compared to its category neighbours, hardcode the canvas size to match a reference thumbnail from the same category instead of relying on `sw`:

```python
# Match zoom of an existing thumbnail (e.g. pasteles-barca-de-avellana-thumb.jpg = 1128px canvas)
canvas_side = 1128   # override auto-sizing
```

**Reference canvas sizes (Pasteles category):**
| Reference product | Canvas size |
|---|---|
| Barca de avellana | 1128 px |
| Barca nata/nuez | 1128 px (matched to avellana) |
| Bracito nata/trufa | 1128 px (matched to avellana) |

When adding a new pasteles thumbnail, compare visually with neighbours and adjust canvas size until the zoom feels consistent. Add the value to the table above.

## Deployment

**Staging** (automatic): Any push to `master` triggers Netlify to rebuild and deploy.

**Production** (manual): Go to GitHub Actions → CI workflow → "Run workflow" on `master`. This builds with Hugo and FTP-syncs `public/` to the hosting server. FTP credentials are stored as GitHub secrets (`FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD`).
