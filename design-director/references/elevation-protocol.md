# Elevation Protocol

A systematic, layer-by-layer process for transforming functional output into designed output.
Work through each layer in order. Do not skip layers. The layers build on each other.

---

## The Core Principle

Every visual output has a functional version (it communicates) and a designed version (it communicates *and* it feels considered). The elevation protocol closes that gap.

Start with a mental model of what the functional version looks like. Identify the 3–4 places where it would look generic. Then solve each one before writing code or content.

---

## LAYER 1: CONCEPT ELEVATION

**Before touching visual decisions, check the concept.**

Ask:
- Is this the right format for what's being communicated? (A table might work better than a chart. A single stat might be more powerful than 6.)
- Is the information architecture right? (What's first? What's last? What's buried that should surface?)
- Is there a central idea — a thesis — that every visual element serves?
- What would be cut if I had to show this in 5 seconds? That thing should be the visual anchor.

**Elevation move:** Identify the single most important insight or action. Make sure the visual hierarchy serves it unambiguously.

---

## LAYER 2: STRUCTURAL ELEVATION

**The underlying grid and organization.**

Ask:
- Is there an explicit grid? (Even a simple 12-column or 4-column grid, just so long as it's there)
- Are elements aligned to the grid, or placed by feel?
- Does the layout have a clear reading path?
- Are sections visually distinct without relying on lines or boxes?

**Elevation moves:**
- Define a column structure before placing elements
- Increase outer margins to at least 8–10% of canvas width
- Separate logical sections with space, not just dividers
- Ensure the layout works if you remove all color — structure should carry hierarchy

---

## LAYER 3: TYPOGRAPHIC ELEVATION

**Typography is the single highest-leverage layer.**

Ask:
- Have I accepted a default font? (If so: change it)
- Is there real contrast between hierarchy levels? (Or are H1 and H2 just slightly different sizes?)
- Are large numerals or display type optically tracked? (Tight-track anything over 32px)
- Is body copy at a comfortable reading width? (45–75 characters per line)
- Are labels, metadata, and captions visually distinct from body copy?

**Elevation moves:**
- Increase the size delta between hierarchy levels (if H1 is 32px, H2 should be ≤20px, not 28px)
- Add optical tracking to display text (-0.02em to -0.04em at large sizes)
- Set line-height intentionally: 1.1–1.2 for headlines, 1.5–1.6 for body
- Choose a second typeface if the piece needs character — one contrasting serif or monospaced font
- Establish and use font weights as a system: regular (400) + medium (500) + bold (700), not random

---

## LAYER 4: COLOR ELEVATION

**Color is used to communicate, not decorate.**

Ask:
- How many colors am I using? (If more than 3 + neutrals: cut)
- Does each color have a consistent meaning? (Accent always means: important. Warning always means: caution.)
- Are my neutrals tinted (warm or cool), or are they pure gray?
- Is there enough contrast everywhere text appears? (Run the WCAG check mentally)
- Am I using color to compensate for weak hierarchy? (If so: fix hierarchy, then remove compensating color)

**Elevation moves:**
- Tint all grays: decide on warm or cool direction, add 5–10% of a hue
- Reduce color count: remove any color that doesn't communicate a distinct meaning
- Check that the accent color appears no more than 10% of total surface area
- If using data color: ensure semantic correctness (sequential vs. categorical scales)
- Ensure background colors have a rational elevation model (darker = deeper, lighter = raised)

---

## LAYER 5: SPATIAL ELEVATION

**Space is what makes professional work feel professional.**

Ask:
- Does this need more breathing room? (Almost always: yes)
- Are spacing values on a consistent scale? (4px/8px increments)
- Is proximity being used to show relationships? (Close = related, distant = separate)
- Are section transitions visually generous?

**Elevation moves:**
- Increase all outer margins by 50%
- Increase padding inside all containers by 50%
- Add 2× spacing before section headings vs. after
- Identify the tightest area — make it less tight
- Apply the 8-point grid to all spacing values

---

## LAYER 6: DETAIL ELEVATION

**The things that separate designed from almost-designed.**

Ask:
- Are border-radius values consistent? (Pick 3 values, use only those)
- Are shadows physically plausible and consistent in depth?
- Are icons from one family, one weight, one style?
- Are all images the same aspect ratio when in grids?
- Do interactive states (hover, active) exist and feel designed?
- Is every number using tabular figures (monospaced numerals)?
- Are decimal points aligned in tables?

**Elevation moves:**
- Audit every rounded corner: establish 3 canonical values and apply consistently
- Check every shadow: same light source, consistent spread-to-blur ratio
- Scan for icon inconsistency: fix any mixing of filled/outlined
- Make sure numbers align: right-align all numerals in tables, use tabular figures

---

## THE FINAL CHECK: The "Squint Test"

Before delivering, squint at the output until it blurs. What do you see?

A well-designed piece should show:
- One clear dominant element (the primary focal point)
- Visible structure (you can see the grid even blurred)
- Rhythm (regular spacing patterns create visual music)
- Restraint (no competing focal points, no visual noise)

If the squint test reveals visual chaos, noise, or ambiguity — elevate more before delivering.

---

## COMMON ELEVATION FAILURES

These are the most frequent signs that elevation was skipped:

| Symptom | Root Cause | Fix |
|---------|-----------|-----|
| Everything is the same size | No hierarchy | Increase size contrast between levels |
| Busy but nothing stands out | Too many accent colors | Reduce to one accent |
| Feels like PowerPoint | Default fonts/colors | Change typeface, establish color system |
| Looks crowded | Insufficient spacing | Double all margins and padding |
| Data is hard to read | No tabular alignment | Right-align numerals, use consistent column widths |
| Charts feel cold | No annotation | Add callouts to key data points |
| Borders everywhere | Weak spatial hierarchy | Remove borders; use space instead |
| Template feeling | Clip art / stock icons | Use geometric shapes or no icons |
| Mismatched elements | Assembled, not designed | Audit every element for visual consistency |

---

## ELEVATION vs. OVER-DESIGN

The goal is not complexity — it's intentionality. Signs you've over-designed:

- Added color to add "interest" without it communicating anything
- Multiple competing focal points
- Decorative elements that don't serve the content
- Type that calls attention to itself rather than the message
- Motion/animation that delays the user getting to the content

When in doubt: remove. The right answer is almost always less.
