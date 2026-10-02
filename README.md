# lucid-brand-icons

Rasterised brand logos (PNG) for Lucid architecture diagrams.

## Why this exists

Lucid fetches an image URL and renders it, but it **does not rasterise SVG**: an
SVG URL returns HTTP 200 and paints nothing on the canvas. Almost every public
brand-logo CDN (simple-icons, gilbarbara/logos, devicon) serves SVG only, so none
of them can be used directly. Lucid also has no image-upload REST endpoint, so
icons cannot be hosted on `images.lucid.app` programmatically.

This repo is the durable raster host. Colour brand SVGs are converted to PNG
once, committed here, and referenced from diagrams as `raw.githubusercontent.com`
URLs.

Lucid stores the URL and re-fetches it on every view rather than copying the
image, so the host stays a dependency for the life of every diagram. That is why
the icons live here rather than behind an on-the-fly conversion proxy.

## Keep this repo public

Lucid fetches these URLs anonymously. If the repo becomes private, every diagram
referencing it loses its icons.

## Adding an icon

For supported logo collections, use the generator in the Cortex Code skill,
which also registers the icon in the resolver catalogue:

    python3 scripts/add_brand.py firebase "google analytics"
    python3 scripts/add_brand.py adjust --domain adjust.com

Skill location: `~/.snowflake/cortex/skills/lucid-architecture-diagrams`

If a brand is absent from that catalogue, search official vendor sources.
Download public artwork, rasterize locally if needed, visually verify it,
record its source and usage terms, and register its durable PNG URL in the
resolver. A missing catalogue entry does not establish that no artwork exists.

## Sources

- Langfuse and Microsoft Foundry: official public vendor assets. See
  [Product sources](PRODUCT-SOURCES.md) for pinned sources and processing details.
- CRM Analytics: Lucid's built-in Salesforce Architecture product icon,
  `SFACRMAnalyticsBlock`, exported alone as a 512x512 PNG on 2026-10-01.
  See [Salesforce sources](SALESFORCE-SOURCES.md). This is a product architecture
  icon, not the Salesforce corporate logo or the separate Tableau logo.
- Full colour logos: gilbarbara/logos and devicon, rasterised via wsrv.nl.
- Brands without a verified higher-quality source: Google's favicon service for the vendor's
  domain. Genuine mark, but low resolution and visibly softer.

Logos are the property of their respective owners and are used nominatively to
identify the products shown in architecture diagrams.
