# How to Use This Vault (Full Guide)

Welcome — this vault, **Personal Knowledge System**, is built to be your second brain for systems & data engineering, learning Rust while keeping Python as your base, and mastering AWS, Spark, Flink, Kafka/Kinesis and distributed systems.

## Vault Philosophy
- Hybrid: **MOC + Zettelkasten**. Use MOCs for navigation and atomic notes for discoverability.
- Fully connected: heavy backlinking and topic maps so relationships appear naturally.
- Project-first: learning by building small projects.
- Spaced repetition: use the Spaced Repetition plugin for flashcards.

## Quick start
1. Convert this master markdown to a folder tree (use `master_to_vault.py` included).
2. Open the created folder in Obsidian.
3. Install recommended plugins: Templates, Daily Notes, Spaced Repetition, Dataview, Excalidraw.
4. Open `00-Start-Here/Study-Dashboard.md` to begin.

## Structure overview
- `00-Start-Here` — onboarding, dashboards, workflows
- `01-Daily-Journal` — daily learning logs
- `02-Study & Learning` — courses, books (DDIA)
- `03-Technical Knowledge Base` — systems, OS, networking, programming primitives
- `04-Data Engineering Library` — storage formats, modeling, processing engines
- `05-Cloud & Platform Notes` — AWS mental models & labs
- `06-Tools & Code Snippets` — Python & Rust snippets, Spark/Flink examples
- `07-Projects` — personal projects and capstones
- `08-Templates` — all templates used across the vault
- `99-Reference` — PDFs, long reads, assets

## Daily workflow
1. Open `01-Daily-Journal/Daily-Template.md` (use Template plugin).
2. Capture discoveries & questions in `00-Inbox`.
3. Move items weekly into atomic notes and link to MOCs.

## Weekly workflow
- Run weekly review in `00-Start-Here/Weekly-Review.md`.
- Update MOCs, add flashcards, plan next week.

## Conversion & import notes
- The conversion script maintains relative paths. Wikilinks use path-based links like `[[03-Technical Knowledge Base/OS - Virtual Memory]]`.
- If you use short link names (like `[[Virtual Memory]]`), Obsidian will try to resolve them; consider keeping consistent filenames.

## How I recommend you use the graph view
- Use MOCs as hubs
- Use filters to focus on `tag:#rust` or `tag:#spark`
- Look at inbound links to decide where to create deeper notes

## Tags & metadata conventions
- Use `#concept` for core ideas, `#project` for projects, `#flashcard` for items to add to spaced repetition.
- For language-specific notes use `#rust` and `#python`.

## Where to start this week
- Open `00-Start-Here/Study-Dashboard.md`
- Start Month 1 tasks under the Month1 section
- Do the first Rust mini-project in `07-Projects/Rust - CLI Tools/README.md`

Happy building — this vault is meant to be *lived in*. Add notes, break things into smaller atomic notes, and link them.
