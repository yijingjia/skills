# Technique Catalog

Specific, named visual techniques organized by what they achieve.
These are moves — concrete decisions you apply, not vague principles.

---

## HIERARCHY TECHNIQUES

### The Anchor Headline
Make one element 3–4× larger than everything else. Not bold — large. This creates an undeniable
entry point. Used by: Bloomberg, The Economist, Linear's marketing pages.
*Apply when:* dashboards, report covers, presentation slides, hero sections.

### Weight Contrast Pairing
Pair a very light weight (300) with a very bold weight (700 or 800) for the same typeface.
Avoid the "medium everything" trap. The contrast between weights communicates structure without color.
*Apply when:* any typography-heavy layout, stat callouts, key figures.

### The Dominant Data Point
Isolate the single most important number or metric. Give it 4× the visual weight of everything else.
Surround it with generous whitespace. Let it breathe. Everything else is context.
*Apply when:* dashboards, financial summaries, KPI reports.

### Progressive Disclosure Layout
Arrange information in layers: the headline message, then supporting figures, then detail.
A viewer who spends 5 seconds gets the main point. 30 seconds gets the full picture.
*Apply when:* executive presentations, summary dashboards, reports.

---

## TYPOGRAPHY TECHNIQUES

### Optical Sizing
Adjust letter-spacing based on size. Large display text (>48px): tighten tracking to -0.02em to -0.04em.
Small text (<14px): loosen tracking to 0.01em to 0.03em. Never use default tracking at display sizes.
*Apply when:* any large headline, display numbers, hero text.

### Contrasting Serif/Sans Pairing
Use a geometric or grotesque sans for UI/data (Inter, DM Sans, Neue Haas Grotesk) paired with
a distinctive serif for headlines (Fraunces, Playfair Display, Canela). The contrast creates
sophistication. The sans handles function; the serif brings character.
*Apply when:* reports, presentations, any piece trying to balance credibility with warmth.

### The Numeric Callout
For any key statistic: set in tabular figures, extra-bold, with a much smaller unit label
(e.g., $47M where "M" is 40% the size of the number). The visual language of data.
*Apply when:* financial dashboards, KPI reports, stat-heavy slides.

### Monospaced Accent
Use a monospaced typeface (iA Writer Mono, JetBrains Mono, Fira Code) for labels, captions,
metadata, or technical details. Creates a deliberate "precision" signal against body text.
*Apply when:* technical dashboards, developer-facing tools, any piece wanting precision aesthetic.

### Small Caps for Labels
Use small caps (font-variant: small-caps or a dedicated small-caps font) for category labels,
column headers, and section markers. More sophisticated than ALL-CAPS; less stiff than uppercase.
*Apply when:* table headers, chart axis labels, navigation items, metadata.

### CJK/Latin Mixed Hierarchy
In Chinese-primary layouts: use letter-spaced all-caps sans-serif for English metadata and labels
(e.g., `CHAPTER 02 · TAKEAWAY`, `SURFACE`, `REAL BUSINESS`) at 10–11px.
Use CJK sans-serif for Chinese headings and body. Insert serif italic Latin for emphasis terms
within Chinese body copy — the contrast in script and weight creates rhythm without relying on color.
*Apply when:* Chinese knowledge presentations, bilingual reports, Mandarin content cards.

---

## COLOR TECHNIQUES

### The 60-30-10 Rule (Applied)
60% neutral (background, large surfaces), 30% supporting tone (secondary surfaces, borders),
10% accent (CTAs, highlights, emphasis). Not color theory — a ratio. Stick to it.
*Apply when:* any interface or document with multiple color areas.

### Tinted Neutrals
Never use pure gray (#808080) when you can use a tinted neutral. Warm: mix gray toward amber.
Cool: mix toward blue-gray. Even a 5% tint makes neutrals feel intentional.
*Apply when:* background colors, card surfaces, sidebar backgrounds.

### Data Color Sequencing
For sequential data scales: use one hue, vary lightness from 10% to 90%.
For categorical data: use hues with equal perceived lightness (so no color "shouts").
Never use rainbow scales (red→yellow→green) for continuous data — they mislead.
*Apply when:* any chart, graph, or heat map.

### Brand Extraction
If the user mentions a company or client, extract their primary brand color and build the
palette around it. Complement with a near-neutral and a pure white. Don't guess — derive.
*Apply when:* client work, branded reports, company-specific dashboards.

### Dark Mode with Elevation
In dark UIs: don't just invert. Use elevation to signal depth — lighter surfaces sit higher.
Base: 10% lightness. Cards: 14%. Modals: 18%. Headers on hover: 22%.
*Apply when:* dark-themed dashboards, developer tools, night-mode documents.

---

## LAYOUT TECHNIQUES

### The Stripe Column
Single dominant left-aligned column with a generous left margin (20–25% of width), right side
used for metadata, timestamps, secondary info. Clean, confident, editorial.
*Apply when:* reports, documentation, long-form data presentation.

### Card Elevation System
Three levels of card depth. Level 1 (default): no shadow, 1px border.
Level 2 (hover/active): subtle shadow (0 2px 8px rgba(0,0,0,0.08)).
Level 3 (modal/overlay): heavier shadow (0 8px 32px rgba(0,0,0,0.16)).
Never more than three levels. Never mix the systems.
*Apply when:* any card-based layout, dashboard widgets, content grids.

### Floating Card on Canvas
White content card (`background: #fff`) hovering over a warm off-white canvas (`#f5f4f0`–`#f0ede6`).
Shadow: `0 8px 32px rgba(0,0,0,0.10)` + optional `0 2px 8px rgba(0,0,0,0.06)`.
The contrast between canvas texture and card white creates a physical, print-like quality.
*Apply when:* editorial presentations, knowledge-content slides, any layout wanting premium "printed on linen" feel.
See: Editorial Presentation exemplar in reference-library.

### The Rule of Thirds Grid
Divide the canvas into a 3×3 grid. Place primary elements at intersection points.
Works for slides, dashboard layouts, report covers, hero sections.
*Apply when:* single-page compositions, cover slides, hero sections.

### Tabular Alignment
In any list or table, align all numbers right, all text left, all status indicators center.
Never mix alignment within a column type. This alone makes data look 10× more professional.
*Apply when:* tables, spreadsheets, data lists, financial statements.

### Generous Margin Signal
Increase margins beyond comfort. What feels like "too much whitespace" is usually right.
Minimum 10% of canvas width as outer margin. Internal section padding: 2× what you first chose.
*Apply when:* reports, premium presentations, anything targeting senior/executive audiences.

---

## SPACING TECHNIQUES

### The 8-Point Grid
All spacing values are multiples of 8px: 8, 16, 24, 32, 40, 48, 56, 64, 80, 96.
For fine-grained control within components, use 4px increments.
Never use arbitrary values like 13px or 22px for spacing.
*Apply when:* HTML/CSS work, digital dashboards, UI-adjacent outputs.

### Proximity Clustering
Group related items closer together than the space between groups.
The gap between logical sections should be 2–3× the gap within sections.
*Apply when:* navigation, form layouts, data groups, content organization.

### Breathing Room Before Headers
Add extra space before headings (1.5–2× the post-heading space). This visually anchors
the heading to what follows, not what precedes, even before the reader consciously notices.
*Apply when:* any document with multiple sections, reports, presentations.

---

## DETAIL TECHNIQUES

### Consistent Radius Scale
Define three radius values: small (3–4px for inputs/tags), medium (8px for cards),
large (12–16px for modals/panels). Never deviate from these three within a piece.
*Apply when:* any HTML/CSS output with rounded corners.

### Hairline Borders
Use 1px borders at 8–12% opacity rather than heavier dividers.
This separates without dividing — a sophisticated visual signal.
*Apply when:* tables, card outlines, section separators.

### The Invisible Grid Reveal
Subtle background patterns (dots or lines at 3% opacity) reveal the underlying grid
and add texture without visual noise. Particularly effective on hero sections or empty states.
*Apply when:* dashboards, cover slides, hero sections with empty space.

### Icon Consistency Rule
Pick one icon family. Pick one weight. Never mix outlined and filled icons. Never mix weights.
If an icon from the set doesn't exist, use text or a simple geometric shape instead.
*Apply when:* any output with multiple icons.

### Micro-Animation Intent
Transitions (when applicable in HTML): 150ms for UI feedback (hover states, buttons),
250ms for content transitions (tabs, accordions), 400ms for contextual animations (modals).
Ease: ease-out for elements entering, ease-in for leaving, ease-in-out for state changes.
*Apply when:* interactive HTML outputs.

---

## COMPOSITION TECHNIQUES

### The Swiss Grid
Strict multi-column grid (usually 12 columns), all content aligned to columns and a baseline grid.
Create asymmetry through column span variation (full width headline, half-width body).
*Apply when:* editorial layouts, reports with mixed content types, formal presentations.

### Visual Breathing
At least 20–30% of any composition should be empty. If the output looks "full," remove something.
Whitespace is the most underused design element. It increases perceived quality.
*Apply when:* every piece, always.

### Focal Hierarchy Trio
Every composition has exactly three focal levels: primary (one element), secondary (2–4 elements),
tertiary (everything else). More than three levels creates confusion.
*Apply when:* slides, dashboards, report pages, any contained layout.
