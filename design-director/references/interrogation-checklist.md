# Design Interrogation Checklist

Run this silently before starting any visual output. You are questioning every assumption.
The goal is to surface the 3–5 decisions that will have the most impact on this specific piece.

---

## 1. Intent & Audience

- Who is the primary viewer? (executive, technical user, general public, client)
- What is the single most important thing they need to understand or feel?
- Is this built to impress, to inform, to persuade, or to be used repeatedly?
- What's the emotional register? (confident, warm, technical, urgent, elegant)
- What would make this person lean in vs. tune out?

## 2. Typography

- What font pairing communicates the right personality? (Have I defaulted to Arial/Helvetica out of laziness?)
- Is there a clear typographic hierarchy? (Can I identify H1, H2, body, caption without needing to check sizes?)
- Are the type sizes actually distinct enough to signal hierarchy, or are they vaguely similar?
- Is the line-height set for readability or left at browser default?
- Are there any orphans, widows, or runts that need fixing?
- Does the body copy column width respect the ~65–75 character optimal line length?
- Am I using font weight as a design tool or just as an emphasis fallback?

## 3. Color

- Does this have a color system or just a collection of colors?
- What is the one dominant color? What are the 1–2 supporting colors?
- Is there enough contrast between text and background? (WCAG AA minimum, prefer AAA)
- Am I using color to communicate meaning or just to decorate?
- Could I remove any color and lose nothing?
- Is the neutral palette warm, cool, or pure gray — and does that match the emotional register?
- If there's data: does the color scale encode the data accurately (not misleadingly)?

## 4. Layout & Grid

- Is there an underlying grid? (Even if invisible, it should exist)
- Are the margins and padding intentional, or defaulted?
- What is the visual entry point? Where does the eye go first?
- Is there a clear path through the layout — primary → secondary → tertiary?
- Are there any elements that feel lost or floating without visual anchoring?
- Is the whitespace active (doing work) or accidental (just leftover)?
- Does the layout breathe, or is it fighting for space?

## 5. Spacing

- Am I using a consistent spacing scale (e.g., multiples of 4 or 8px)?
- Is proximity being used to show relationships? (Things that belong together should be close)
- Does vertical rhythm exist in the typographic layout?
- Are section breaks visually clear without requiring dividers/lines?
- Is any element crowded against its container edge?

## 6. Visual Hierarchy & Emphasis

- If I squint at this, what stands out? Is that what should stand out?
- Am I emphasizing 5 things (which means I'm emphasizing nothing)?
- Is the most important number, fact, or action the visually dominant element?
- Are supporting elements clearly subordinate?
- Do call-to-action elements (buttons, key figures, headlines) have enough visual weight?

## 7. Details & Polish

- Are all the radii (border-radius) consistent across similar elements?
- Are shadow depths consistent and physically plausible (light source coherent)?
- Are icon weights consistent throughout? (Never mix filled and outlined icons)
- Are all images the same aspect ratio when displayed in a grid?
- Is alignment pixel-perfect, or are there 1–2px inconsistencies?
- Are interactive states (hover, focus, active) designed?
- Does anything look like it was pasted in from somewhere else?

## 8. The "Is This Designed?" Test

Ask yourself honestly:
- Would a professional designer be comfortable putting their name on this?
- Does this look like it was made for this specific purpose, or does it look like a template?
- Is there at least one design choice here that shows intentionality — something that says "I decided this"?
- If the client saw this next to a competitor's work, would it hold its own?

---

## Priority Triage

After running the full checklist, identify your top 3 leverage points:

1. **Highest impact** — The one thing that will most change how this piece is perceived
2. **Biggest risk** — The default choice that would make this look generic
3. **The detail** — The small thing that signals craft and intentionality

Solve these three before anything else.
