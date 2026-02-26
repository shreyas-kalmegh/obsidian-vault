# AGENTS.md - Data Modelling Folder Rules

These rules apply to work inside:
`04-Data Engineering Library/Data Modelling`

## Primary Objective
Produce medium-depth, practical data modeling notes that are:
- accurate
- internally consistent
- example-driven where needed

## Content Standards
1. Do not write cheatsheet-only content unless explicitly asked.
2. Prefer this structure:
   - `Overview`
   - core concepts/design decisions
   - examples
   - common mistakes
   - practical checklist
3. Keep sections concise and scannable.
4. Add or preserve Obsidian wiki-links to related notes.

## Consistency Rules
1. Grain must be explicit when discussing facts.
2. SCD strategy must be justified per attribute.
3. Keep Kimball and Lakehouse framing compatible:
   - Kimball dimensional models are valid in Gold.
   - Medallion is data-quality layering, not a replacement for dimensional modeling.
4. Use consistent terms for Bronze/Silver/Gold semantics.

## Example Guidance
1. Include concrete examples when explaining:
   - fact type choice
   - SCD handling
   - late-arriving data
   - CDC/incremental merges
2. Use short SQL snippets where they improve clarity.

## Token-Efficient Workflow
For new sessions, read only:
1. `04-Data Engineering Library/Data Modelling/CONTEXT.md`
2. `04-Data Engineering Library/Data Modelling/session-handoff.md`
3. user-specified target files

Avoid full-repo scans unless the task requires them.
