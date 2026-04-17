---
primary_hex: "#0045DB"
secondary_hex: "#0F2CC9"
dark_hex: "#141A2E"
light_blue_hex: "#6C95F5"
lighter_blue_hex: "#BBDAFF"
gray_hex: "#838D96"
light_gray_hex: "#C1CCD3"
lightest_gray_hex: "#DFE8ED"
background_hex: "#FFFFFF"
text_hex: "#141A2E"
text_light_hex: "#FFFFFF"
cta_red_hex: "#EF3333"
display_font_family: "Burlingame Pro"
display_font_alt: "Saira"
headline_font_family: "FS Silas Slab"
headline_font_alt: "Zilla Slab"
body_font_family: "Sans Beam"
body_font_alt: "Lexend"
brand_name: "Anderson Lock & Safe"
tagline: "Securing Arizona Since 1966"
founded: 1966
canva_brand_kit_id: "kAGLyB_BxbM"
canva_brand_kit_name: "New Anderson Lock and Safe"
source: "Prolific Brand Design — brand-guidelines.pdf (12 pages, 2023)"
---

# Anderson Lock & Safe — Visual Style Guide

**Source of truth:** Official brand guidelines by Prolific Brand Design (2023). Front-matter tokens drive `tools/image_generator.py` and Canva renders. Keep everything here in sync with [brand-guidelines.pdf](../brand-guidelines.pdf).

## Color Palette

### Primary Blues
| Token | Hex | Pantone | CMYK | Use |
|------|-----|---------|------|-----|
| Primary Blue | `#0045DB` | 286 C | C100 M80 Y0 K0 | Dominant brand color — logos, headers, buttons |
| Secondary Blue | `#0F2CC9` | Blue 072 C | C100 M80 Y0 K10 | Alternate primary, layering with primary |
| Deep Navy | `#141A2E` | 289 C | C89 M80 Y52 K65 | Body text on light backgrounds, 1-color logo variant |

### Light Blues
| Token | Hex | Pantone | Use |
|------|-----|---------|-----|
| Mid Blue | `#6C95F5` | 2727 C | Accent, hover states, secondary graphics |
| Sky Blue | `#BBDAFF` | 278 C | Soft backgrounds, secondary buttons (Button 3) |

### Grays
| Token | Hex | Pantone | Use |
|------|-----|---------|-----|
| Gray | `#838D96` | 4137 C | Neutral text, secondary buttons (Button 2) |
| Light Gray | `#C1CCD3` | 7543 C | Dividers, disabled states |
| Lightest Gray | `#DFE8ED` | 5455 C | Soft backgrounds |
| White | `#FFFFFF` | — | Reverse logos, light backgrounds |

### Utility
| Token | Hex | Use |
|------|-----|-----|
| CTA Red | `#EF3333` | **Call-to-action buttons only** (Button 4). Never elsewhere. |

## Typography

Three official typefaces — always use these in order of priority. Free Google Fonts alternatives are listed for web/Canva when the paid fonts aren't installed.

| Role | Primary | Free Alternative |
|------|---------|------------------|
| Logo / Headline / Display | **Burlingame Pro** | [Saira](https://fonts.google.com/specimen/Saira) |
| Logo / Headline / Display | **FS Silas Slab** | [Zilla Slab](https://fonts.google.com/specimen/Zilla+Slab) |
| Body | **Sans Beam** | [Lexend](https://fonts.google.com/specimen/Lexend) |

### Heading Hierarchy
- **H1:** Burlingame (blue, large, sentence case)
- **H2:** Burlingame (uppercase)
- **H3:** FS Silas Slab (sentence case)
- **H4:** Burlingame Condensed (uppercase)
- **H5:** FS Silas Slab (uppercase)
- **H6:** Burlingame Condensed (uppercase, small)
- **Display:** FS Silas Slab (uppercase, bold, blue)
- **Body:** Sans Beam Semi-Light

### Buttons
| Button | Background | Text | Use |
|--------|-----------|------|-----|
| Button 1 | Primary Blue `#0045DB` | White | Primary CTA |
| Button 2 | Gray `#838D96` | White | Secondary/neutral |
| Button 3 | Sky Blue `#BBDAFF` | Primary Blue | Tertiary / inverted |
| Button 4 | CTA Red `#EF3333` | White | **Call-to-action only** |

## Logo Usage

### Four Official Formats
1. **LOGO_BLUE_1 / WHITE_1 / BLACK_1** — Stacked: padlock-A mark above "Anderson LOCK & SAFE"
2. **LOGO_BLUE_2 / WHITE_2 / BLACK_2** — Horizontal: mark left of wordmark
3. **LOGO_BLUE_3 / WHITE_3 / BLACK_3** — Mark only (padlock-A symbol)
4. **LOGO_BLUE_4 / WHITE_4 / BLACK_4** — Wordmark only ("Anderson LOCK & SAFE")

### Color Variants
- **Full Color (BLUE)** — Primary Blue `#0045DB`. Default for light backgrounds.
- **Reverse (WHITE)** — Solid white. For dark / photo / blue backgrounds.
- **1-Color (BLACK)** — Deep Navy `#141A2E`. For single-color print applications.

### TM Usage
Add the ™ only when the symbol will be readable at final size. Files: `LOGO_BLUE_1_TM`, `LOGO_BLUE_TM`.

## Improper Usage — DO NOT

1. **Clear space** — always keep a buffer of negative space around the logo
2. **Effects** — no drop shadows, glows, bevels, or filters
3. **Obstruction** — never cover the logo with another object
4. **Colors** — never alter the logo color (no green, red, purple logos)
5. **Transparency** — never apply opacity to the logo
6. **Distortion** — never stretch or squish; scale proportionally
7. **Added type** — never add text inside or touching the logo
8. **Alterations** — no outlines, additional colors, or modifications
9. **Orientation** — never rotate from original position
10. **Editing** — never delete or change elements within the graphic

## Patterns & Backgrounds

Pattern swatches (repeating padlock-A and "Anderson" wordmark tiles) are available in the native Illustrator files and may be used by designers only. Pattern swatches can be rendered in any brand blue, navy, gray, or white. Photos with blue tint overlay (`#0045DB` at ~70% opacity) are the signature brand photo treatment.

## Tile Formats (for social)

The agent picks one of these when the post format is "infographic":

| Format | Use when | Tool subcommand |
|--------|----------|-----------------|
| Tip card | A single insight, opinion, or "did you know" | `tip-card` |
| Stat card | A single number with context | `stat-card` |
| Q&A card | A common customer question + answer | `qa-card` |
| Numbered list | 3-5 things (checklist, warning signs, steps) | `numbered-list` |
| Before/After | Physical work photos showing transformation | `before-after` |

## Sizing

- **Instagram feed**: 1080x1080 (square) or 1080x1350 (portrait)
- **Instagram Reel cover / Story**: 1080x1920 (vertical)
- **Facebook / LinkedIn feed**: 1080x1080 default

## Emoji / Hashtag Conventions

- **Facebook**: no hashtags, zero or 1 emoji max.
- **LinkedIn**: 5-7 branded hashtags (e.g., #CommercialLocksmith, #PhoenixBusiness, #FacilitiesManagement, #SecurityInfrastructure, #MasterKeySystems), 0-1 emoji.
- **Instagram**: 8-12 hashtags (mix of broad + niche), 1-2 emoji maximum — never in the first line.

## Named Programs

- **"Free Key Audit"** — for property managers: we'll inventory every key, keyway, and master level in the building. Use in LinkedIn tips, blog CTAs.
- **Medeco Upgrade Program** — confirm program name with Garrett.

When either appears in a caption, surface it in bold on the graphic tile too.

## Voice Rules Recap (from [anderson-lock-and-safe-ai-guidelines.md](../anderson-lock-and-safe-ai-guidelines.md))

- 95% commercial — property managers, facilities teams, GCs, schools, government
- Never compete on price. Lead with manpower, reliability, expertise, 60+ year heritage.
- Facebook: casual first-person. LinkedIn: professional B2B with discussion questions. Instagram: visual-first, short caption.
- Reference **specific** details from the referenced video/photo/job. Never generic-locksmith filler.

## When to use Canva vs. the Pillow generator

- **Canva (`canva_designer.py`)** — preferred for polished public posts, uses Garrett's brand kit templates, supports drag-in photography.
- **Pillow (`image_generator.py`)** — fallback when Canva is unavailable, when the agent is generating a lot of tiles rapidly, or for quick text-only formats (stat cards, Q&A).
