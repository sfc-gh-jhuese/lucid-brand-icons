# Snowflake Icon Provenance

Both icons come from Snowflake's publicly downloadable 2026 presentation template:

https://www.snowflake.com/wp-content/themes/snowflake/assets/img/brand-guidelines/downloads/Snowflake_Template_2026.potx.zip

Source landing page: https://www.snowflake.com/brand-guidelines/

| PNG | Template Location | Processing |
| --- | --- | --- |
| `png/snowflake-tables.png` | Slide 69, shape 2389, under Snowflake Tables | Original vector paths extracted; white changed to permitted Snowflake Blue; locally rasterized with transparent background. |
| `png/snowflake-openflow.png` | Slide 74, shape 3222, labeled Openflow | Original vector paths extracted and locally rasterized with transparent background. |
| `png/snowflake-cortex.png` | Slide 74, shape 3192, labeled Snowflake Cortex | Vector paths converted with `tools/extract_template_icon.py`; Snowflake Blue; 512 px. |
| `png/snowpark-containers.png` | Slide 74, shape 3170, labeled Snowpark Containers | Same process. |
| `png/snowpark-ml-registry.png` | Slide 74, shape 3232, labeled Snowpark ML Registry | Same process. |
| `png/snowflake-trail.png` | Slide 74, shape 3193, labeled Snowflake Trail | Same process. |
| `png/snowflake-document-ai.png` | Slide 74, shape 3027, labeled Document AI | Same process. |
| `png/snowflake-search.png` | Slide 76 (general icons), shape 3562, labeled Search | Same process. |
| `png/snowflake-sql-analysts.png` | Slide 78 (general icons), shape 4082, labeled SQL Analysts | Same process. |
| `png/snowflake-metadata.png` | Slide 78 (general icons), shape 4286, labeled Metadata | Same process. |
| `png/snowflake-iceberg-tables.png` | Slide 74, shape 3064, labeled Iceberg Tables | Same process (DrawingML group paths rendered locally, even-odd fill, trimmed). |

The template has no dedicated marks for Cortex Analyst, Cortex Agent or Semantic
Views. Diagrams use the labeled general icons above (SQL Analysts, Snowflake
Cortex, Metadata) with the product name next to the icon. Snowflake Blue is one of
the colors the template's icon guidance (slide 72) permits. Extraction was
verified by re-extracting Openflow and comparing it with the published asset.

Artwork remains Snowflake's. This records provenance, not a grant of additional trademark or redistribution rights. No customer data or internal presentation content is included.
## Snowflake 2026 template, slide 74 product feature icons (added 2026-10-14)
- Source: Snowflake 2026 corporate template, public brand-guidelines download https://www.snowflake.com/wp-content/themes/snowflake/assets/img/brand-guidelines/downloads/Snowflake_Template_2026.potx.zip, slide 74 'Icons: Snowflake Product Features', REV 3.5.26.
- Processing: original DrawingML vector paths converted to SVG locally (drawingml_to_svg.py v2, bounding box from shape xfrm), rasterised, white render background removed from the corners. No recolouring.
- Files:
  - `png/snowflake-gen2-warehouse.png` - Gen2 Warehouse (512 x 512)
  - `png/snowflake-adaptive-warehouse.png` - Adaptive Warehouse (512 x 512)
  - `png/snowflake-snowpark-warehouse.png` - Snowpark-optimized Warehouse (512 x 512)
  - `png/snowflake-interactive-warehouse.png` - Interactive Warehouse (512 x 512)
  - `png/snowflake-horizon.png` - Snowflake Horizon (512 x 512)
  - `png/snowflake-external-tables.png` - External Tables (512 x 512)
  - `png/snowflake-hybrid-tables.png` - Hybrid Tables (512 x 512)
  - `png/snowflake-chat-apis.png` - Chat APIs (512 x 512)
  - `png/snowflake-interactive-tables.png` - Interactive Tables (512 x 512)
  - `png/snowflake-native-app.png` - Snowflake Native App (512 x 512)
  - `png/snowflake-spark-connect.png` - Spark Connect (512 x 512)
  - `png/snowflake-snowconvert-ai.png` - SnowConvert AI (512 x 512)
  - `png/snowflake-snowpark-ml-modeling.png` - Snowpark ML Modeling (512 x 512)
  - `png/snowflake-universal-search.png` - Universal Search (512 x 512)
